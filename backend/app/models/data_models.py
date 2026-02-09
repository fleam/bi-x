from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.sources import DataSource

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
    model_type = Column(String(50), default="star")  # star, snowflake
    data_sets = Column(JSON, nullable=False)  # list of data sets
    relationships = Column(JSON, nullable=False)  # list of relationships
    dimensions = Column(JSON, nullable=False)  # list of dimensions
    measures = Column(JSON, nullable=False)  # list of measures
    hierarchies = Column(JSON, nullable=True)  # list of hierarchies
    grain = Column(Text, nullable=True)  # data grain
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    # 由于一个数据模型关联多个数据集，不再使用外键关系
    # 而是在 data_sets 字段中存储数据集ID和角色
