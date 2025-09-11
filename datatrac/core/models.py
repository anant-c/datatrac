# datatrac/core/models.py
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Dataset(Base):
    __tablename__ = "datasets"

    hash = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    source = Column(String, nullable=True)
    local_path = Column(String, unique=True)
    registry_path = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
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

class Lineage(Base):
    __tablename__ = "lineage"

    parent_hash = Column(String, ForeignKey("datasets.hash"), primary_key=True)
    child_hash = Column(String, ForeignKey("datasets.hash"), primary_key=True)
    
    parent = relationship("Dataset", foreign_keys=[parent_hash], back_populates="children")
    child = relationship("Dataset", foreign_keys=[child_hash], back_populates="parents")