from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class FieldConfig(BaseModel):
    name: str
    type: str
    alias: Optional[str] = None
    is_dimension: Optional[bool] = False
    is_measure: Optional[bool] = False

class VisualConfig(BaseModel):
    tables: List[str]
    fields: List[FieldConfig]
    filters: Optional[List[Dict[str, Any]]] = None
    groups: Optional[List[str]] = None
    aggregations: Optional[Dict[str, str]] = None

class DataSetBase(BaseModel):
    name: str = Field(..., description="数据集名称")
    description: Optional[str] = Field(None, description="数据集描述")
    data_source_id: int = Field(..., description="数据源ID")
    creation_mode: str = Field(..., description="创建模式: visual, sql")
    sql_query: Optional[str] = Field(None, description="SQL查询语句")
    visual_config: Optional[VisualConfig] = Field(None, description="可视化配置")
    fields: List[FieldConfig] = Field(..., description="字段列表")
    refresh_interval: Optional[int] = Field(300, description="数据刷新间隔(秒)")

class DataSetCreate(DataSetBase):
    pass

class DataSetUpdate(BaseModel):
    name: Optional[str] = Field(None, description="数据集名称")
    description: Optional[str] = Field(None, description="数据集描述")
    data_source_id: Optional[int] = Field(None, description="数据源ID")
    creation_mode: Optional[str] = Field(None, description="创建模式: visual, sql")
    sql_query: Optional[str] = Field(None, description="SQL查询语句")
    visual_config: Optional[VisualConfig] = Field(None, description="可视化配置")
    fields: Optional[List[FieldConfig]] = Field(None, description="字段列表")
    refresh_interval: Optional[int] = Field(None, description="数据刷新间隔(秒)")
    is_active: Optional[bool] = Field(None, description="是否启用")

class DataSetResponse(DataSetBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DimensionConfig(BaseModel):
    name: str
    field: str
    type: str
    hierarchy: Optional[str] = None

class MeasureConfig(BaseModel):
    name: str
    field: str
    aggregation: str
    format: Optional[str] = None

class HierarchyConfig(BaseModel):
    name: str
    levels: List[str]

class DataSetConfig(BaseModel):
    id: Optional[int] = None
    data_set_id: int
    role: Optional[str] = "dimension"  # fact, dimension
    alias: Optional[str] = None

class RelationshipConfig(BaseModel):
    source_data_set: int
    source_field: str
    target_data_set: int
    target_field: str
    join_type: str = "inner"  # inner, left, right

class DataModelBase(BaseModel):
    name: str = Field(..., description="数据模型名称")
    description: Optional[str] = Field(None, description="数据模型描述")
    model_type: str = Field("star", description="模型类型: star, snowflake")
    data_sets: List[DataSetConfig] = Field(..., description="数据集列表")
    relationships: List[RelationshipConfig] = Field(..., description="数据集关系列表")
    dimensions: List[DimensionConfig] = Field(..., description="维度列表")
    measures: List[MeasureConfig] = Field(..., description="度量列表")
    hierarchies: Optional[List[HierarchyConfig]] = Field(None, description="层次结构列表")
    grain: Optional[str] = Field(None, description="数据粒度")

class DataModelCreate(DataModelBase):
    pass

class DataModelUpdate(BaseModel):
    name: Optional[str] = Field(None, description="数据模型名称")
    description: Optional[str] = Field(None, description="数据模型描述")
    model_type: Optional[str] = Field(None, description="模型类型: star, snowflake")
    data_sets: Optional[List[DataSetConfig]] = Field(None, description="数据集列表")
    relationships: Optional[List[RelationshipConfig]] = Field(None, description="数据集关系列表")
    dimensions: Optional[List[DimensionConfig]] = Field(None, description="维度列表")
    measures: Optional[List[MeasureConfig]] = Field(None, description="度量列表")
    hierarchies: Optional[List[HierarchyConfig]] = Field(None, description="层次结构列表")
    grain: Optional[str] = Field(None, description="数据粒度")
    is_active: Optional[bool] = Field(None, description="是否启用")

class DataModelResponse(DataModelBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
