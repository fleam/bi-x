from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class DataSourceBase(BaseModel):
    name: str = Field(..., description="数据源名称")
    type: str = Field(..., description="数据源类型: database, excel, api")
    db_type: Optional[str] = Field(None, description="数据库类型: mysql, oracle, postgresql")
    host: Optional[str] = Field(None, description="数据库主机地址")
    port: Optional[int] = Field(None, description="数据库端口")
    database: Optional[str] = Field(None, description="数据库名称")
    username: Optional[str] = Field(None, description="用户名")
    password: Optional[str] = Field(None, description="密码")
    file_path: Optional[str] = Field(None, description="Excel文件路径")
    api_url: Optional[str] = Field(None, description="API接口地址")
    api_method: Optional[str] = Field(None, description="API请求方法: get, post")
    api_headers: Optional[Dict[str, Any]] = Field(None, description="API请求头")
    api_body: Optional[Dict[str, Any]] = Field(None, description="API请求体")
    connection_pool: Optional[int] = Field(10, description="连接池大小")
    refresh_interval: Optional[int] = Field(300, description="数据刷新间隔(秒)")

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    name: Optional[str] = Field(None, description="数据源名称")
    type: Optional[str] = Field(None, description="数据源类型: database, excel, api")
    db_type: Optional[str] = Field(None, description="数据库类型: mysql, oracle, postgresql")
    host: Optional[str] = Field(None, description="数据库主机地址")
    port: Optional[int] = Field(None, description="数据库端口")
    database: Optional[str] = Field(None, description="数据库名称")
    username: Optional[str] = Field(None, description="用户名")
    password: Optional[str] = Field(None, description="密码")
    file_path: Optional[str] = Field(None, description="Excel文件路径")
    api_url: Optional[str] = Field(None, description="API接口地址")
    api_method: Optional[str] = Field(None, description="API请求方法: get, post")
    api_headers: Optional[Dict[str, Any]] = Field(None, description="API请求头")
    api_body: Optional[Dict[str, Any]] = Field(None, description="API请求体")
    connection_pool: Optional[int] = Field(None, description="连接池大小")
    refresh_interval: Optional[int] = Field(None, description="数据刷新间隔(秒)")
    is_active: Optional[bool] = Field(None, description="是否启用")

class DataSourceResponse(DataSourceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TestConnectionRequest(BaseModel):
    type: str = Field(..., description="数据源类型: database, excel, api")
    db_type: Optional[str] = Field(None, description="数据库类型: mysql, oracle, postgresql")
    host: Optional[str] = Field(None, description="数据库主机地址")
    port: Optional[int] = Field(None, description="数据库端口")
    database: Optional[str] = Field(None, description="数据库名称")
    username: Optional[str] = Field(None, description="用户名")
    password: Optional[str] = Field(None, description="密码")
    file_path: Optional[str] = Field(None, description="Excel文件路径")
    api_url: Optional[str] = Field(None, description="API接口地址")
    api_method: Optional[str] = Field(None, description="API请求方法: get, post")
    api_headers: Optional[Dict[str, Any]] = Field(None, description="API请求头")
    api_body: Optional[Dict[str, Any]] = Field(None, description="API请求体")

class TestConnectionResponse(BaseModel):
    success: bool
    message: str
