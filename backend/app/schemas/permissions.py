from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# 权限相关Schema
class PermissionBase(BaseModel):
    name: str = Field(..., description="权限名称")
    code: str = Field(..., description="权限代码，如 dashboard:view")
    description: Optional[str] = Field(None, description="权限描述")

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, description="权限名称")
    code: Optional[str] = Field(None, description="权限代码")
    description: Optional[str] = Field(None, description="权限描述")
    is_active: Optional[bool] = Field(None, description="是否启用")

class PermissionResponse(PermissionBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 角色相关Schema
class RoleBase(BaseModel):
    name: str = Field(..., description="角色名称")
    description: Optional[str] = Field(None, description="角色描述")

class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = Field([], description="权限ID列表")

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, description="角色名称")
    description: Optional[str] = Field(None, description="角色描述")
    permission_ids: Optional[List[int]] = Field(None, description="权限ID列表")
    is_active: Optional[bool] = Field(None, description="是否启用")

class RoleResponse(RoleBase):
    id: int
    is_active: bool
    permissions: List[PermissionResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 用户相关Schema
class UserBase(BaseModel):
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    name: str = Field(..., description="姓名")

class UserCreate(UserBase):
    password: str = Field(..., description="密码")
    role_ids: Optional[List[int]] = Field([], description="角色ID列表")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    name: Optional[str] = Field(None, description="姓名")
    password: Optional[str] = Field(None, description="密码")
    role_ids: Optional[List[int]] = Field(None, description="角色ID列表")
    is_active: Optional[bool] = Field(None, description="是否启用")

class UserResponse(UserBase):
    id: int
    is_active: bool
    roles: List[RoleResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 登录相关Schema
class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# 资源权限相关Schema
class ResourceBase(BaseModel):
    name: str = Field(..., description="资源名称")
    type: str = Field(..., description="资源类型: dashboard, chart, dataset")
    resource_id: int = Field(..., description="对应资源的ID")
    is_public: Optional[bool] = Field(False, description="是否公开")

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, description="资源名称")
    is_public: Optional[bool] = Field(None, description="是否公开")

class ResourceResponse(ResourceBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
