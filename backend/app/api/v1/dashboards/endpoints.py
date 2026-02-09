from fastapi import APIRouter, HTTPException
from app.schemas.dashboards import ChartCreate, ChartUpdate, ChartResponse, DashboardCreate, DashboardUpdate, DashboardResponse
from app.services.dashboards import chart_service, dashboard_service

router = APIRouter()

# 图表相关接口
@router.post("/charts", response_model=ChartResponse)
async def create_chart(chart: ChartCreate):
    try:
        return await chart_service.create(chart)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/charts", response_model=list[ChartResponse])
async def get_charts():
    try:
        return await chart_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/charts/{chart_id}", response_model=ChartResponse)
async def get_chart(chart_id: int):
    try:
        return await chart_service.get_by_id(chart_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/charts/{chart_id}", response_model=ChartResponse)
async def update_chart(chart_id: int, chart: ChartUpdate):
    try:
        return await chart_service.update(chart_id, chart)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/charts/{chart_id}")
async def delete_chart(chart_id: int):
    try:
        await chart_service.delete(chart_id)
        return {"message": "图表删除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 仪表盘相关接口
@router.post("/dashboards", response_model=DashboardResponse)
async def create_dashboard(dashboard: DashboardCreate):
    try:
        return await dashboard_service.create(dashboard)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboards", response_model=list[DashboardResponse])
async def get_dashboards():
    try:
        return await dashboard_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(dashboard_id: int):
    try:
        return await dashboard_service.get_by_id(dashboard_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def update_dashboard(dashboard_id: int, dashboard: DashboardUpdate):
    try:
        return await dashboard_service.update(dashboard_id, dashboard)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/dashboards/{dashboard_id}")
async def delete_dashboard(dashboard_id: int):
    try:
        await dashboard_service.delete(dashboard_id)
        return {"message": "仪表盘删除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
