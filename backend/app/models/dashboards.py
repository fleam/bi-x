from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Dashboard(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    layout = Column(JSON, nullable=False)  # 仪表盘布局配置
    widgets = Column(JSON, nullable=False)  # 仪表盘组件配置
    refresh_interval = Column(Integer, default=300)  # seconds
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Chart(Base):
    __tablename__ = "charts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    chart_type = Column(String(50), nullable=False)  # line, bar, pie, etc.
    data_model_id = Column(Integer, ForeignKey("data_models.id"), nullable=False)
    dimensions = Column(JSON, nullable=False)  # 维度配置
    measures = Column(JSON, nullable=False)  # 度量配置
    filters = Column(JSON, nullable=True)  # 筛选条件
    style = Column(JSON, nullable=True)  # 样式配置
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    data_model = relationship("DataModel", backref="charts")
