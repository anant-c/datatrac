# datatrac/core/manager.py
import subprocess
import getpass
from pathlib import Path
from sqlalchemy.orm import Session

from . import models, utils
from .config import REMOTE_TARGET, REMOTE_STORAGE_PATH

def get_current_user():
    return getpass.getuser()

def run_command(command: list[str]):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        error_message = result.stderr or result.stdout
        raise RuntimeError(f"Command failed: {' '.join(command)}\nError: {error_message.strip()}")
    return result.stdout

class DataManager:
    def __init__(self, db: Session):
        self.db = db

    def find_by_hash(self, file_hash: str):
        return self.db.query(models.Dataset).filter_by(hash=file_hash).first()

    def find_all(self):
        return self.db.query(models.Dataset).order_by(models.Dataset.created_at.desc()).all()

    def find_local_path_for_user(self, file_hash: str):
        user = get_current_user()
        copy = self.db.query(models.LocalCopy).filter_by(dataset_hash=file_hash, user_identifier=user).first()
        return Path(copy.local_path) if copy and Path(copy.local_path).exists() else None

    def _get_or_create_local_copy(self, dataset_hash: str, local_path: str):
        user = get_current_user()
        copy = self.db.query(models.LocalCopy).filter_by(dataset_hash=dataset_hash, user_identifier=user).first()
        if copy:
            copy.local_path = local_path
        else:
            copy = models.LocalCopy(dataset_hash=dataset_hash, user_identifier=user, local_path=local_path)
            self.db.add(copy)
        self.db.commit()

    def push_dataset(self, local_path_str: str, source: str | None = None):
        local_path = Path(local_path_str).resolve()
        if not local_path.exists():
            raise FileNotFoundError(f"File not found: {local_path}")
        file_hash = utils.hash_file(str(local_path))
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            print("Dataset not found in global registry. Uploading...")
            registry_path = f"{REMOTE_STORAGE_PATH}/{file_hash}{local_path.suffix}"
            run_command(["scp", str(local_path), f"{REMOTE_TARGET}:{registry_path}"])
            dataset = models.Dataset(hash=file_hash, name=local_path.name, source=source, registry_path=registry_path)
            self.db.add(dataset)
        else:
            print(f"Dataset with hash {file_hash[:8]}... already exists in global registry.")
        self._get_or_create_local_copy(file_hash, str(local_path))
        return dataset

    def download_dataset(self, file_hash: str, destination_dir: str = "."):
        # Feature: Prevent re-download
        existing_path = self.find_local_path_for_user(file_hash)
        if existing_path:
            return existing_path, "Dataset already exists locally at the path below."
        
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            raise FileNotFoundError(f"Dataset with hash {file_hash} not found in the registry.")
        
        local_destination = Path(destination_dir).resolve() / dataset.name
        remote_source = f"{REMOTE_TARGET}:{dataset.registry_path}"
        print(f"Downloading from {REMOTE_TARGET}...")
        run_command(["scp", remote_source, str(local_destination)])
        self._get_or_create_local_copy(file_hash, str(local_destination))
        return local_destination, "Download complete."

    def delete_dataset(self, file_hash: str):
        """Admin Function: Deletes a dataset from the remote registry and DB."""
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            return False, f"Dataset with hash {file_hash} not found."
        print(f"Deleting remote file: {dataset.registry_path}")
        run_command(["ssh", REMOTE_TARGET, f"rm {dataset.registry_path}"])
        self.db.delete(dataset)
        self.db.commit()
        return True, "Dataset and all associated records have been deleted from the registry."

    def delete_local_copy(self, file_hash: str):
        """User Function: Deletes a dataset from the local machine only."""
        user = get_current_user()
        copy = self.db.query(models.LocalCopy).filter_by(dataset_hash=file_hash, user_identifier=user).first()
        if not copy:
            return False, "You do not have a local record for this dataset."
        
        local_file = Path(copy.local_path)
        if not local_file.exists():
            self.db.delete(copy) # Clean up dangling record
            self.db.commit()
            return False, "Local file not found, but stale record was cleaned up."
        
        local_file.unlink()
        self.db.delete(copy)
        self.db.commit()
        return True, f"Successfully deleted local file and record for: {local_file}"

    def create_lineage(self, parent_hash: str, child_hash: str) -> models.Lineage:
        """Creates a lineage link between two datasets."""
        parent = self.find_by_hash(parent_hash)
        if not parent:
            raise ValueError(f"Parent dataset with hash {parent_hash} not found.")
        
        child = self.find_by_hash(child_hash)
        if not child:
            raise ValueError(f"Child dataset with hash {child_hash} not found.")

        lineage_link = models.Lineage(parent_hash=parent_hash, child_hash=child_hash)
        self.db.add(lineage_link)
        self.db.commit()
        self.db.refresh(lineage_link)
        return lineage_link
    
    def get_lineage(self, file_hash: str) -> dict:
        """Retrieves all parents and children for a given dataset hash."""
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            raise FileNotFoundError(f"Dataset with hash {file_hash} not found.")

        parents = [
            {"name": link.parent.name, "hash": link.parent.hash}
            for link in dataset.parents
        ]
        children = [
            {"name": link.child.name, "hash": link.child.hash}
            for link in dataset.children
        ]
        
        return {"parents": parents, "children": children}