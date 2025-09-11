# datatrac/core/models.py
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from .db import Base

class Dataset(Base):
    __tablename__ = "datasets"

    hash = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    source = Column(String, nullable=True)
    registry_path = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    

    # NEW: The flag for soft deletes. Defaults to True for all new datasets.
    is_active = Column(Boolean, default=True, nullable=False)

    # This relationship links a dataset to all its local copies.
    # When a Dataset is deleted, all its LocalCopy records are also deleted.
    copies = relationship("LocalCopy", back_populates="dataset", cascade="all, delete-orphan")
    
    # Relationships for lineage
    parents = relationship(
        "Lineage",
        foreign_keys="[Lineage.child_hash]",
        back_populates="child",
        cascade="all, delete-orphan"
    )
    children = relationship(
        "Lineage",
        foreign_keys="[Lineage.parent_hash]",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

class LocalCopy(Base):
    __tablename__ = "local_copies"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_hash = Column(String, ForeignKey("datasets.hash"), nullable=False)
    user_identifier = Column(String, nullable=False, index=True) # e.g., 'anant'
    local_path = Column(String, nullable=False)
    
    dataset = relationship("Dataset", back_populates="copies")

class Lineage(Base):
    __tablename__ = "lineage"

    parent_hash = Column(String, ForeignKey("datasets.hash"), primary_key=True)
    child_hash = Column(String, ForeignKey("datasets.hash"), primary_key=True)
    
    parent = relationship("Dataset", foreign_keys=[parent_hash], back_populates="children")
    child = relationship("Dataset", foreign_keys=[child_hash], back_populates="parents")