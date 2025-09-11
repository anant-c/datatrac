# datatrac/api/schemas.py
import datetime
from pydantic import BaseModel

# Schema for creating a lineage link
class LineageCreate(BaseModel):
    parent_hash: str
    child_hash: str

# Base schema for a dataset, used for sharing common fields
class DatasetBase(BaseModel):
    hash: str
    name: str
    source: str | None = None
    registry_path: str
    created_at: datetime.datetime
    is_active: bool
    size_bytes: int | None = None
    download_count: int
    last_downloaded_at: datetime.datetime | None = None

# Full schema for returning a dataset from the API
# It includes orm_mode = True to work directly with SQLAlchemy models
class Dataset(DatasetBase):
    class Config:
        from_attributes = True # Replaces orm_mode in Pydantic v2   