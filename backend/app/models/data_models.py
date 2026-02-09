from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class DataSet(Base):
    __tablename__ = "data_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    creation_mode = Column(String(50), nullable=False)  # visual, sql
    sql_query = Column(Text, nullable=True)  # for sql mode
    visual_config = Column(JSON, nullable=True)  # for visual mode
    fields = Column(JSON, nullable=False)  # list of fields
    refresh_interval = Column(Integer, default=300)  # seconds
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    data_source = relationship("DataSource", backref="data_sets")

class DataModel(Base):
    __tablename__ = "data_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    data_set_id = Column(Integer, ForeignKey("data_sets.id"), nullable=False)
    dimensions = Column(JSON, nullable=False)  # list of dimensions
    measures = Column(JSON, nullable=False)  # list of measures
    hierarchies = Column(JSON, nullable=True)  # list of hierarchies
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    data_set = relationship("DataSet", backref="data_models")
