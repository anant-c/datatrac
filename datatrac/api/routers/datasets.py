# datatrac/api/routers/datasets.py
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Header
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from datatrac.core.db import get_db
from datatrac.core.manager import DataManager
from .. import schemas

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
)

# Endpoint to list all available datasets
@router.get("/", response_model=List[schemas.Dataset])
def list_datasets(db: Session = Depends(get_db)):
    """
    Retrieve a list of all datasets visible to the user.
    This mirrors the `datatrac fetch -a` command.
    """
    manager = DataManager(db)
    datasets = manager.find_all()
    return datasets

# Endpoint to get details for a single dataset
@router.get("/{dataset_hash}", response_model=schemas.Dataset)
def get_dataset_details(dataset_hash: str, db: Session = Depends(get_db)):
    """
    Get detailed information for a single dataset by its hash.
    Mirrors `datatrac fetch {hash}`.
    """
    manager = DataManager(db)
    dataset = manager.find_by_hash(dataset_hash)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

# Endpoint to upload a new dataset
@router.post("/upload", response_model=schemas.Dataset)
async def upload_dataset(
    source: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a new dataset file. Mirrors `datatrac push`.
    The file is sent as multipart/form-data.
    """
    # Save the uploaded file to a temporary path
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    manager = DataManager(db)
    try:
        dataset, _ = manager.push_dataset(temp_path, source=source)
        return dataset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to trigger a download (updates stats)
@router.post("/{dataset_hash}/download", response_model=schemas.Dataset)
def trigger_download(dataset_hash: str, db: Session = Depends(get_db)):
    """
    Triggers the download logic for a dataset, which increments its
    download count and updates the timestamp.

    Note: This endpoint does not stream the file back. It simulates a
    download event and returns the updated dataset metadata.
    """
    manager = DataManager(db)
    try:
        # The download_dataset method now handles stats updates
        # We don't need the returned path in the API context
        dataset = manager.find_by_hash(dataset_hash)
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
        dataset.download_count += 1
        dataset.last_downloaded_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(dataset)
        return dataset
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
# Endpoint to delete a dataset (Admin)
@router.delete("/{dataset_hash}")
def delete_dataset(
    dataset_hash: str,
    x_admin_password: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Deregisters a dataset from the registry. Requires an admin password
    passed in the 'X-Admin-Password' header.
    """
    from datatrac.cli.commands.delete import ADMIN_PASSWORD # Reuse password
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Invalid admin password")
        
    manager = DataManager(db)
    success, message = manager.delete_dataset(dataset_hash)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}

@router.get("/{dataset_hash}/lineage", response_model=schemas.LineageResponse)
def get_dataset_lineage(dataset_hash: str, db: Session = Depends(get_db)):
    """
    Get the parent and child lineage for a specific dataset.
    """
    manager = DataManager(db)
    try:
        lineage_data = manager.get_lineage(dataset_hash)
        return lineage_data
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))