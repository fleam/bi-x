from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    model_type = Column(String(100), nullable=False)  # 分析模型类型
    parameters = Column(JSON, nullable=True)  # 分析参数
    data_source = Column(JSON, nullable=True)  # 数据源配置
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    result = Column(JSON, nullable=True)  # 分析结果
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator = relationship("User")

class PredictionModel(Base):
    __tablename__ = "prediction_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    model_type = Column(String(100), nullable=False)  # 预测模型类型
    parameters = Column(JSON, nullable=True)  # 模型参数
    training_data = Column(JSON, nullable=True)  # 训练数据配置
    model_path = Column(String(500), nullable=True)  # 模型存储路径
    status = Column(String(50), default="created")  # created, training, trained, failed
    metrics = Column(JSON, nullable=True)  # 模型评估指标
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator = relationship("User")

class Macro(Base):
    __tablename__ = "macros"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    code = Column(Text, nullable=False)  # 宏代码
    parameters = Column(JSON, nullable=True)  # 宏参数
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator = relationship("User")

class SystemMonitor(Base):
    __tablename__ = "system_monitors"

    id = Column(Integer, primary_key=True, index=True)
    component = Column(String(255), nullable=False)  # 监控组件
    metric = Column(String(255), nullable=False)  # 监控指标
    value = Column(JSON, nullable=False)  # 指标值
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(100), nullable=False)  # 集成类型
    config = Column(JSON, nullable=False)  # 集成配置
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
