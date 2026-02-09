from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# AI分析相关Schema
class AIAnalysisBase(BaseModel):
    name: str = Field(..., description="分析名称")
    description: Optional[str] = Field(None, description="分析描述")
    model_type: str = Field(..., description="分析模型类型")
    parameters: Optional[Dict[str, Any]] = Field(None, description="分析参数")
    data_source: Optional[Dict[str, Any]] = Field(None, description="数据源配置")

class AIAnalysisCreate(AIAnalysisBase):
    pass

class AIAnalysisUpdate(BaseModel):
    name: Optional[str] = Field(None, description="分析名称")
    description: Optional[str] = Field(None, description="分析描述")
    parameters: Optional[Dict[str, Any]] = Field(None, description="分析参数")
    data_source: Optional[Dict[str, Any]] = Field(None, description="数据源配置")

class AIAnalysisResponse(AIAnalysisBase):
    id: int
    status: str
    result: Optional[Dict[str, Any]] = Field(None, description="分析结果")
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 预测模型相关Schema
class PredictionModelBase(BaseModel):
    name: str = Field(..., description="模型名称")
    description: Optional[str] = Field(None, description="模型描述")
    model_type: str = Field(..., description="预测模型类型")
    parameters: Optional[Dict[str, Any]] = Field(None, description="模型参数")
    training_data: Optional[Dict[str, Any]] = Field(None, description="训练数据配置")

class PredictionModelCreate(PredictionModelBase):
    pass

class PredictionModelUpdate(BaseModel):
    name: Optional[str] = Field(None, description="模型名称")
    description: Optional[str] = Field(None, description="模型描述")
    parameters: Optional[Dict[str, Any]] = Field(None, description="模型参数")
    training_data: Optional[Dict[str, Any]] = Field(None, description="训练数据配置")

class PredictionModelResponse(PredictionModelBase):
    id: int
    status: str
    model_path: Optional[str] = Field(None, description="模型存储路径")
    metrics: Optional[Dict[str, Any]] = Field(None, description="模型评估指标")
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 宏相关Schema
class MacroBase(BaseModel):
    name: str = Field(..., description="宏名称")
    description: Optional[str] = Field(None, description="宏描述")
    code: str = Field(..., description="宏代码")
    parameters: Optional[Dict[str, Any]] = Field(None, description="宏参数")

class MacroCreate(MacroBase):
    pass

class MacroUpdate(BaseModel):
    name: Optional[str] = Field(None, description="宏名称")
    description: Optional[str] = Field(None, description="宏描述")
    code: Optional[str] = Field(None, description="宏代码")
    parameters: Optional[Dict[str, Any]] = Field(None, description="宏参数")
    is_active: Optional[bool] = Field(None, description="是否启用")

class MacroResponse(MacroBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 系统监控相关Schema
class SystemMonitorBase(BaseModel):
    component: str = Field(..., description="监控组件")
    metric: str = Field(..., description="监控指标")
    value: Dict[str, Any] = Field(..., description="指标值")

class SystemMonitorCreate(SystemMonitorBase):
    pass

class SystemMonitorResponse(SystemMonitorBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# 集成相关Schema
class IntegrationBase(BaseModel):
    name: str = Field(..., description="集成名称")
    description: Optional[str] = Field(None, description="集成描述")
    type: str = Field(..., description="集成类型")
    config: Dict[str, Any] = Field(..., description="集成配置")

class IntegrationCreate(IntegrationBase):
    pass

class IntegrationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="集成名称")
    description: Optional[str] = Field(None, description="集成描述")
    config: Optional[Dict[str, Any]] = Field(None, description="集成配置")
    is_active: Optional[bool] = Field(None, description="是否启用")

class IntegrationResponse(IntegrationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
