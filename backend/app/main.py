from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import sources, data_models, visualization, dashboards
from app.api.v1.permissions import router as permissions_router
from app.api.v1.advanced import router as advanced_router
from app.core.database import engine, Base
from app.models import permissions, advanced
from app.services.permissions import create_default_admin
import asyncio

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建默认管理员用户
asyncio.create_task(create_default_admin())

app = FastAPI(
    title="BI报表工具API",
    description="提供数据源管理、数据建模、可视化分析等功能",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应设置具体的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(sources.router, prefix="/api/v1/sources", tags=["数据源管理"])
app.include_router(data_models.router, prefix="/api/v1", tags=["数据建模"])
app.include_router(visualization.router, prefix="/api/v1/visualization", tags=["可视化分析"])
app.include_router(dashboards.router, prefix="/api/v1", tags=["仪表盘管理"])
app.include_router(permissions_router, prefix="/api/v1", tags=["权限管理"])
app.include_router(advanced_router, prefix="/api/v1", tags=["高级分析"])

@app.get("/")
async def root():
    return {"message": "BI报表工具API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
