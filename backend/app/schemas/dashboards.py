from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ChartBase(BaseModel):
    name: str = Field(..., description="图表名称")
    description: Optional[str] = Field(None, description="图表描述")
    chart_type: str = Field(..., description="图表类型: line, bar, pie, etc.")
    data_model_id: int = Field(..., description="数据模型ID")
    dimensions: List[Dict[str, Any]] = Field(..., description="维度配置")
    measures: List[Dict[str, Any]] = Field(..., description="度量配置")
    filters: Optional[List[Dict[str, Any]]] = Field(None, description="筛选条件")
    style: Optional[Dict[str, Any]] = Field(None, description="样式配置")

class ChartCreate(ChartBase):
    pass

class ChartUpdate(BaseModel):
    name: Optional[str] = Field(None, description="图表名称")
    description: Optional[str] = Field(None, description="图表描述")
    chart_type: Optional[str] = Field(None, description="图表类型: line, bar, pie, etc.")
    data_model_id: Optional[int] = Field(None, description="数据模型ID")
    dimensions: Optional[List[Dict[str, Any]]] = Field(None, description="维度配置")
    measures: Optional[List[Dict[str, Any]]] = Field(None, description="度量配置")
    filters: Optional[List[Dict[str, Any]]] = Field(None, description="筛选条件")
    style: Optional[Dict[str, Any]] = Field(None, description="样式配置")
    is_active: Optional[bool] = Field(None, description="是否启用")

class ChartResponse(ChartBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class WidgetConfig(BaseModel):
    id: str
    type: str  # chart, metric, text
    chart_id: Optional[int] = None
    position: Dict[str, Any]
    size: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None

class LayoutConfig(BaseModel):
    rows: int
    cols: int
    gap: int

class DashboardBase(BaseModel):
    name: str = Field(..., description="仪表盘名称")
    description: Optional[str] = Field(None, description="仪表盘描述")
    layout: LayoutConfig = Field(..., description="仪表盘布局配置")
    widgets: List[WidgetConfig] = Field(..., description="仪表盘组件配置")
    refresh_interval: Optional[int] = Field(300, description="数据刷新间隔(秒)")

class DashboardCreate(DashboardBase):
    pass

class DashboardUpdate(BaseModel):
    name: Optional[str] = Field(None, description="仪表盘名称")
    description: Optional[str] = Field(None, description="仪表盘描述")
    layout: Optional[LayoutConfig] = Field(None, description="仪表盘布局配置")
    widgets: Optional[List[WidgetConfig]] = Field(None, description="仪表盘组件配置")
    refresh_interval: Optional[int] = Field(None, description="数据刷新间隔(秒)")
    is_active: Optional[bool] = Field(None, description="是否启用")

class DashboardResponse(DashboardBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
