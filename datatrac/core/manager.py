import subprocess
import getpass
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from datetime import datetime, timezone

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
        """
        Finds all datasets that are either active in the registry OR 
        that the current user has a local copy of.
        """
        user = get_current_user()
        
        # Subquery to get all dataset hashes the current user has locally
        local_hashes_subquery = select(models.LocalCopy.dataset_hash).where(
            models.LocalCopy.user_identifier == user
        )

        # Main query
        query = self.db.query(models.Dataset).filter(
            or_(
                models.Dataset.is_active == True,
                models.Dataset.hash.in_(local_hashes_subquery)
            )
        )
        return query.order_by(models.Dataset.created_at.desc()).all()

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
        was_uploaded = False  # Initialize flag

        if not dataset:
            print("Dataset not found in global registry. Uploading...")
            registry_path = f"{REMOTE_STORAGE_PATH}/{file_hash}{local_path.suffix}"
            run_command(["scp", str(local_path), f"{REMOTE_TARGET}:{registry_path}"])

            # NEW: Get file size during push
            file_size = local_path.stat().st_size

            dataset = models.Dataset(
                hash=file_hash, 
                name=local_path.name, 
                source=source, 
                registry_path=registry_path,
                size_bytes=file_size
            )
            self.db.add(dataset)
            was_uploaded = True # Set flag to True on new upload
        else:
            print(f"Dataset with hash {file_hash[:8]}... already exists in global registry.")

        self._get_or_create_local_copy(file_hash, str(local_path))
        
        # Return both the dataset object and the flag
        return dataset, was_uploaded

    def download_dataset(self, file_hash: str, destination_dir: str = "."):
        existing_path = self.find_local_path_for_user(file_hash)
        if existing_path:
            return existing_path, "Dataset already exists locally at the path below."
        
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            raise FileNotFoundError(f"Dataset with hash {file_hash} not found in the registry.")
        
        # NEW: Prevent downloading a deregistered file
        if not dataset.is_active:
            raise FileNotFoundError("Cannot download: This dataset has been deregistered by an admin and is no longer available on the server.")
        
        local_destination = Path(destination_dir).resolve() / dataset.name
        remote_source = f"{REMOTE_TARGET}:{dataset.registry_path}"
        print(f"Downloading from {REMOTE_TARGET}...")
        run_command(["scp", remote_source, str(local_destination)])
        self._get_or_create_local_copy(file_hash, str(local_destination))


        dataset.download_count += 1
        dataset.last_downloaded_at = datetime.now(timezone.utc)
        self.db.commit()
        return local_destination, "Download complete."

    def delete_dataset(self, file_hash: str):
        """
        Admin Function: Deregisters a dataset. It marks it as inactive
        and deletes the file from the remote server.
        """
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            return False, f"Dataset with hash {file_hash} not found."
            
        if not dataset.is_active:
            return False, "This dataset has already been deregistered."

        print(f"Deleting remote file: {dataset.registry_path}")
        run_command(["ssh", REMOTE_TARGET, f"rm {dataset.registry_path}"])
        
        # UPDATE instead of DELETE
        dataset.is_active = False
        self.db.commit()
        return True, "Dataset has been deregistered. Users with local copies can still see it."

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