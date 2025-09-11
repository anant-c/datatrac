# datatrac/core/manager.py
import shutil
import subprocess
from pathlib import Path
from sqlalchemy.orm import Session
from . import models, utils
from .config import REMOTE_TARGET, REMOTE_STORAGE_PATH

def run_command(command: list[str]):
    """Helper function to run a shell command and check for errors."""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        error_message = result.stderr or result.stdout
        raise RuntimeError(f"Command failed: {' '.join(command)}\nError: {error_message.strip()}")
    return result.stdout

class DataManager:
    def __init__(self, db: Session):
        self.db = db

    def find_by_hash(self, file_hash: str) -> models.Dataset | None:
        """Finds a dataset by its SHA256 hash."""
        return self.db.query(models.Dataset).filter(models.Dataset.hash == file_hash).first()

    def find_all(self):
        """Returns all datasets in the registry."""
        return self.db.query(models.Dataset).all()

    def push_dataset(self, local_path_str: str, source: str | None = None) -> models.Dataset:
        """Adds a dataset to the remote registry via SCP."""
        local_path = Path(local_path_str).resolve()
        if not local_path.exists():
            raise FileNotFoundError(f"File not found at: {local_path}")

        file_hash = utils.hash_file(str(local_path))
        
        existing_dataset = self.find_by_hash(file_hash)
        if existing_dataset:
            print(f"Dataset with hash {file_hash[:8]}... already exists.")
            return existing_dataset

        file_extension = local_path.suffix
        remote_filename = f"{file_hash}{file_extension}"
        remote_path_full = f"{REMOTE_STORAGE_PATH}/{remote_filename}"

        # Use SCP to copy the file to the remote server
        print(f"Uploading to {REMOTE_TARGET}...")
        scp_command = ["scp", str(local_path), f"{REMOTE_TARGET}:{remote_path_full}"]
        run_command(scp_command)
        print("Upload complete.")

        new_dataset = models.Dataset(
            hash=file_hash,
            name=local_path.name,
            source=source,
            local_path=str(local_path), # The original local path
            registry_path=remote_path_full, # The path on the remote server
        )
        self.db.add(new_dataset)
        self.db.commit()
        self.db.refresh(new_dataset)
        return new_dataset

    def download_dataset(self, file_hash: str, destination_dir: str = ".") -> Path:
        """Downloads a dataset from the remote registry to a local path."""
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            raise FileNotFoundError(f"Dataset with hash {file_hash} not found in the database.")
        
        local_destination = Path(destination_dir).resolve() / dataset.name
        remote_source = f"{REMOTE_TARGET}:{dataset.registry_path}"

        print(f"Downloading from {REMOTE_TARGET} to {local_destination}...")
        scp_command = ["scp", remote_source, str(local_destination)]
        run_command(scp_command)
        print("Download complete.")
        return local_destination


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

    def delete_dataset(self, file_hash: str) -> bool:
        """Deletes a dataset from the remote registry and the database."""
        dataset = self.find_by_hash(file_hash)
        if not dataset:
            return False
        
        # Use SSH to remove the file on the remote server
        print(f"Deleting remote file: {dataset.registry_path}")
        ssh_command = ["ssh", REMOTE_TARGET, f"rm {dataset.registry_path}"]
        run_command(ssh_command)
        
        # Remove from database
        self.db.delete(dataset)
        self.db.commit()
        return True