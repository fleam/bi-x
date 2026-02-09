from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.database import SessionLocal
from app.schemas.permissions import (
    UserCreate, UserUpdate, UserResponse, LoginRequest, LoginResponse,
    RoleCreate, RoleUpdate, RoleResponse,
    PermissionCreate, PermissionUpdate, PermissionResponse,
    ResourceCreate, ResourceUpdate, ResourceResponse
)
from app.services.permissions import user_service, role_service, permission_service, resource_service
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 认证相关函数
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_service.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user

# 认证相关端点
@router.post("/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    user = await user_service.authenticate(login_data.username, login_data.password)
    access_token = await user_service.create_access_token(data={"sub": user.username})
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )

# 权限相关端点
@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(permission: PermissionCreate, current_user: UserResponse = Depends(get_current_user)):
    return await permission_service.create(permission)

@router.get("/permissions", response_model=List[PermissionResponse])
async def get_permissions(current_user: UserResponse = Depends(get_current_user)):
    return await permission_service.get_all()

@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(permission_id: int, current_user: UserResponse = Depends(get_current_user)):
    return await permission_service.get_by_id(permission_id)

@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
async def update_permission(permission_id: int, permission_update: PermissionUpdate, current_user: UserResponse = Depends(get_current_user)):
    return await permission_service.update(permission_id, permission_update)

@router.delete("/permissions/{permission_id}")
async def delete_permission(permission_id: int, current_user: UserResponse = Depends(get_current_user)):
    await permission_service.delete(permission_id)
    return {"message": "权限删除成功"}

# 角色相关端点
@router.post("/roles", response_model=RoleResponse)
async def create_role(role: RoleCreate, current_user: UserResponse = Depends(get_current_user)):
    return await role_service.create(role)

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles():
    return await role_service.get_all()

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, current_user: UserResponse = Depends(get_current_user)):
    return await role_service.get_by_id(role_id)

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role_update: RoleUpdate, current_user: UserResponse = Depends(get_current_user)):
    return await role_service.update(role_id, role_update)

@router.delete("/roles/{role_id}")
async def delete_role(role_id: int, current_user: UserResponse = Depends(get_current_user)):
    await role_service.delete(role_id)
    return {"message": "角色删除成功"}

# 用户相关端点
@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: UserResponse = Depends(get_current_user)):
    return await user_service.create(user)

@router.get("/users", response_model=List[UserResponse])
async def get_users():
    return await user_service.get_all()

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, current_user: UserResponse = Depends(get_current_user)):
    return await user_service.get_by_id(user_id)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, current_user: UserResponse = Depends(get_current_user)):
    return await user_service.update(user_id, user_update)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: UserResponse = Depends(get_current_user)):
    await user_service.delete(user_id)
    return {"message": "用户删除成功"}

# 资源相关端点
@router.post("/resources", response_model=ResourceResponse)
async def create_resource(resource: ResourceCreate, current_user: UserResponse = Depends(get_current_user)):
    return await resource_service.create(resource, current_user.id)

@router.get("/resources", response_model=List[ResourceResponse])
async def get_resources(current_user: UserResponse = Depends(get_current_user)):
    return await resource_service.get_all()

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, current_user: UserResponse = Depends(get_current_user)):
    return await resource_service.get_by_id(resource_id)

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource_update: ResourceUpdate, current_user: UserResponse = Depends(get_current_user)):
    return await resource_service.update(resource_id, resource_update)

@router.delete("/resources/{resource_id}")
async def delete_resource(resource_id: int, current_user: UserResponse = Depends(get_current_user)):
    await resource_service.delete(resource_id)
    return {"message": "资源删除成功"}
