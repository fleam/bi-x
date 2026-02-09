from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class PivotAnalysisRequest(BaseModel):
    data_model_id: int = Field(..., description="数据模型ID")
    dimensions: List[str] = Field(..., description="维度字段列表")
    measures: List[str] = Field(..., description="度量字段列表")
    filters: Optional[List[Dict[str, Any]]] = Field(None, description="筛选条件列表")
    sort_by: Optional[str] = Field(None, description="排序字段")
    sort_order: Optional[str] = Field("asc", description="排序顺序: asc, desc")

class PivotAnalysisResponse(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    columns: List[str]
    message: Optional[str] = None

class AdhocQueryRequest(BaseModel):
    data_set_id: int = Field(..., description="数据集ID")
    fields: List[str] = Field(..., description="查询字段列表")
    filters: Optional[List[Dict[str, Any]]] = Field(None, description="筛选条件列表")
    limit: Optional[int] = Field(1000, description="返回数据行数限制")
    offset: Optional[int] = Field(0, description="分页偏移量")

class AdhocQueryResponse(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    total: int
    message: Optional[str] = None

class SpreadsheetRequest(BaseModel):
    data_set_id: int = Field(..., description="数据集ID")
    template_id: Optional[int] = Field(None, description="模板ID")
    parameters: Optional[Dict[str, Any]] = Field(None, description="参数列表")

class SpreadsheetResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None
