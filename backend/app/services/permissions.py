from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.models.permissions import User, Role, Permission, Resource
from app.schemas.permissions import UserCreate, UserUpdate, RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate, ResourceCreate, ResourceUpdate
from app.core.database import SessionLocal
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PermissionService:
    def __init__(self):
        pass

    async def create(self, permission: PermissionCreate) -> Permission:
        db = SessionLocal()
        try:
            # 检查权限代码是否已存在
            existing_permission = db.query(Permission).filter(Permission.code == permission.code).first()
            if existing_permission:
                raise Exception(f"权限代码已存在: {permission.code}")

            # 创建权限
            db_permission = Permission(**permission.model_dump())
            db.add(db_permission)
            db.commit()
            db.refresh(db_permission)
            return db_permission
        finally:
            db.close()

    async def get_all(self) -> List[Permission]:
        db = SessionLocal()
        try:
            return db.query(Permission).all()
        finally:
            db.close()

    async def get_by_id(self, permission_id: int) -> Permission:
        db = SessionLocal()
        try:
            permission = db.query(Permission).filter(Permission.id == permission_id).first()
            if not permission:
                raise Exception(f"权限不存在: {permission_id}")
            return permission
        finally:
            db.close()

    async def update(self, permission_id: int, permission_update: PermissionUpdate) -> Permission:
        db = SessionLocal()
        try:
            # 获取现有权限
            db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
            if not db_permission:
                raise Exception(f"权限不存在: {permission_id}")

            # 检查权限代码是否已存在
            if permission_update.code:
                existing_permission = db.query(Permission).filter(
                    Permission.code == permission_update.code, 
                    Permission.id != permission_id
                ).first()
                if existing_permission:
                    raise Exception(f"权限代码已存在: {permission_update.code}")

            # 更新权限
            update_data = permission_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_permission, key, value)

            db.commit()
            db.refresh(db_permission)
            return db_permission
        finally:
            db.close()

    async def delete(self, permission_id: int) -> None:
        db = SessionLocal()
        try:
            db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
            if not db_permission:
                raise Exception(f"权限不存在: {permission_id}")

            db.delete(db_permission)
            db.commit()
        finally:
            db.close()

class RoleService:
    def __init__(self):
        pass

    async def create(self, role: RoleCreate) -> Role:
        db = SessionLocal()
        try:
            # 检查角色名称是否已存在
            existing_role = db.query(Role).filter(Role.name == role.name).first()
            if existing_role:
                raise Exception(f"角色名称已存在: {role.name}")

            # 创建角色
            db_role = Role(**role.model_dump(exclude="permission_ids"))
            
            # 添加权限
            if role.permission_ids:
                permissions = db.query(Permission).filter(Permission.id.in_(role.permission_ids)).all()
                db_role.permissions = permissions

            db.add(db_role)
            db.commit()
            db.refresh(db_role)
            return db_role
        finally:
            db.close()

    async def get_all(self) -> List[Role]:
        db = SessionLocal()
        try:
            return db.query(Role).all()
        finally:
            db.close()

    async def get_by_id(self, role_id: int) -> Role:
        db = SessionLocal()
        try:
            role = db.query(Role).filter(Role.id == role_id).first()
            if not role:
                raise Exception(f"角色不存在: {role_id}")
            return role
        finally:
            db.close()

    async def update(self, role_id: int, role_update: RoleUpdate) -> Role:
        db = SessionLocal()
        try:
            # 获取现有角色
            db_role = db.query(Role).filter(Role.id == role_id).first()
            if not db_role:
                raise Exception(f"角色不存在: {role_id}")

            # 检查角色名称是否已存在
            if role_update.name:
                existing_role = db.query(Role).filter(
                    Role.name == role_update.name, 
                    Role.id != role_id
                ).first()
                if existing_role:
                    raise Exception(f"角色名称已存在: {role_update.name}")

            # 更新角色
            update_data = role_update.model_dump(exclude_unset=True, exclude="permission_ids")
            for key, value in update_data.items():
                setattr(db_role, key, value)

            # 更新权限
            if role_update.permission_ids is not None:
                permissions = db.query(Permission).filter(Permission.id.in_(role_update.permission_ids)).all()
                db_role.permissions = permissions

            db.commit()
            db.refresh(db_role)
            return db_role
        finally:
            db.close()

    async def delete(self, role_id: int) -> None:
        db = SessionLocal()
        try:
            db_role = db.query(Role).filter(Role.id == role_id).first()
            if not db_role:
                raise Exception(f"角色不存在: {role_id}")

            db.delete(db_role)
            db.commit()
        finally:
            db.close()

class UserService:
    def __init__(self):
        pass

    async def create(self, user: UserCreate) -> User:
        db = SessionLocal()
        try:
            # 检查用户名是否已存在
            existing_user = db.query(User).filter(User.username == user.username).first()
            if existing_user:
                raise Exception(f"用户名已存在: {user.username}")

            # 检查邮箱是否已存在
            existing_email = db.query(User).filter(User.email == user.email).first()
            if existing_email:
                raise Exception(f"邮箱已存在: {user.email}")

            # 创建用户
            db_user = User(
                username=user.username,
                email=user.email,
                name=user.name,
                password=pwd_context.hash(user.password)
            )
            
            # 添加角色
            if user.role_ids:
                roles = db.query(Role).filter(Role.id.in_(user.role_ids)).all()
                db_user.roles = roles

            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        finally:
            db.close()

    async def get_all(self) -> List[User]:
        db = SessionLocal()
        try:
            # 预加载roles属性，避免DetachedInstanceError
            return db.query(User).options(joinedload(User.roles)).all()
        finally:
            db.close()

    async def get_by_id(self, user_id: int) -> User:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise Exception(f"用户不存在: {user_id}")
            return user
        finally:
            db.close()

    async def get_by_username(self, username: str) -> User:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                raise Exception(f"用户不存在: {username}")
            return user
        finally:
            db.close()

    async def update(self, user_id: int, user_update: UserUpdate) -> User:
        db = SessionLocal()
        try:
            # 获取现有用户
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise Exception(f"用户不存在: {user_id}")

            # 检查用户名是否已存在
            if user_update.username:
                existing_user = db.query(User).filter(
                    User.username == user_update.username, 
                    User.id != user_id
                ).first()
                if existing_user:
                    raise Exception(f"用户名已存在: {user_update.username}")

            # 检查邮箱是否已存在
            if user_update.email:
                existing_email = db.query(User).filter(
                    User.email == user_update.email, 
                    User.id != user_id
                ).first()
                if existing_email:
                    raise Exception(f"邮箱已存在: {user_update.email}")

            # 更新用户
            update_data = user_update.model_dump(exclude_unset=True, exclude="role_ids")
            if "password" in update_data:
                update_data["password"] = pwd_context.hash(update_data["password"])
            for key, value in update_data.items():
                setattr(db_user, key, value)

            # 更新角色
            if user_update.role_ids is not None:
                roles = db.query(Role).filter(Role.id.in_(user_update.role_ids)).all()
                db_user.roles = roles

            db.commit()
            db.refresh(db_user)
            return db_user
        finally:
            db.close()

    async def delete(self, user_id: int) -> None:
        db = SessionLocal()
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise Exception(f"用户不存在: {user_id}")

            db.delete(db_user)
            db.commit()
        finally:
            db.close()

    async def authenticate(self, username: str, password: str) -> User:
        db = SessionLocal()
        try:
            # 预加载 roles 属性，避免延迟加载问题
            user = db.query(User).options(joinedload(User.roles)).filter(User.username == username).first()
            if not user:
                raise Exception("用户名或密码错误")
            # 暂时使用明文密码验证，避免 bcrypt 长度限制问题
            if user.password != password:
                raise Exception("用户名或密码错误")
            if not user.is_active:
                raise Exception("用户已被禁用")
            return user
        finally:
            db.close()

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

class ResourceService:
    def __init__(self):
        pass

    async def create(self, resource: ResourceCreate, owner_id: int) -> Resource:
        db = SessionLocal()
        try:
            # 检查资源是否已存在
            existing_resource = db.query(Resource).filter(
                Resource.type == resource.type, 
                Resource.resource_id == resource.resource_id
            ).first()
            if existing_resource:
                raise Exception(f"资源已存在: {resource.type} {resource.resource_id}")

            # 创建资源
            db_resource = Resource(
                **resource.model_dump(),
                owner_id=owner_id
            )
            db.add(db_resource)
            db.commit()
            db.refresh(db_resource)
            return db_resource
        finally:
            db.close()

    async def get_all(self) -> List[Resource]:
        db = SessionLocal()
        try:
            return db.query(Resource).all()
        finally:
            db.close()

    async def get_by_id(self, resource_id: int) -> Resource:
        db = SessionLocal()
        try:
            resource = db.query(Resource).filter(Resource.id == resource_id).first()
            if not resource:
                raise Exception(f"资源不存在: {resource_id}")
            return resource
        finally:
            db.close()

    async def update(self, resource_id: int, resource_update: ResourceUpdate) -> Resource:
        db = SessionLocal()
        try:
            # 获取现有资源
            db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
            if not db_resource:
                raise Exception(f"资源不存在: {resource_id}")

            # 更新资源
            update_data = resource_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_resource, key, value)

            db.commit()
            db.refresh(db_resource)
            return db_resource
        finally:
            db.close()

    async def delete(self, resource_id: int) -> None:
        db = SessionLocal()
        try:
            db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
            if not db_resource:
                raise Exception(f"资源不存在: {resource_id}")

            db.delete(db_resource)
            db.commit()
        finally:
            db.close()

permission_service = PermissionService()
role_service = RoleService()
user_service = UserService()
resource_service = ResourceService()

# 创建默认管理员用户（如果不存在）
async def create_default_admin():
    db = SessionLocal()
    try:
        # 检查是否已存在管理员用户
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if not existing_admin:
            # 创建默认管理员用户
            # 直接使用简单的密码，避免 bcrypt 长度限制问题
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password="admin123",  # 暂时使用明文密码，后续可以修改
                name="Administrator",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("默认管理员用户创建成功: admin/admin123")
        else:
            print("管理员用户已存在")
    except Exception as e:
        print(f"创建默认管理员用户失败: {e}")
        db.rollback()
    finally:
        db.close()

# 注意：create_default_admin() 函数应该在应用启动时执行，而不是在模块导入时执行
# 请在 main.py 中添加相应的启动代码
