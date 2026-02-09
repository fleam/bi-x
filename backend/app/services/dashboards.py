from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.dashboards import Chart, Dashboard
from app.schemas.dashboards import ChartCreate, ChartUpdate, DashboardCreate, DashboardUpdate
from app.core.database import SessionLocal

class ChartService:
    def __init__(self):
        pass

    async def create(self, chart: ChartCreate) -> Chart:
        db = SessionLocal()
        try:
            # 验证数据模型是否存在
            from app.models.data_models import DataModel
            db_data_model = db.query(DataModel).filter(DataModel.id == chart.data_model_id).first()
            if not db_data_model:
                raise Exception(f"数据模型不存在: {chart.data_model_id}")

            # 创建图表
            db_chart = Chart(**chart.model_dump())
            db.add(db_chart)
            db.commit()
            db.refresh(db_chart)
            return db_chart
        finally:
            db.close()

    async def get_all(self) -> List[Chart]:
        db = SessionLocal()
        try:
            return db.query(Chart).all()
        finally:
            db.close()

    async def get_by_id(self, chart_id: int) -> Chart:
        db = SessionLocal()
        try:
            chart = db.query(Chart).filter(Chart.id == chart_id).first()
            if not chart:
                raise Exception(f"图表不存在: {chart_id}")
            return chart
        finally:
            db.close()

    async def update(self, chart_id: int, chart_update: ChartUpdate) -> Chart:
        db = SessionLocal()
        try:
            # 获取现有图表
            db_chart = db.query(Chart).filter(Chart.id == chart_id).first()
            if not db_chart:
                raise Exception(f"图表不存在: {chart_id}")

            # 验证数据模型是否存在
            if chart_update.data_model_id:
                from app.models.data_models import DataModel
                db_data_model = db.query(DataModel).filter(DataModel.id == chart_update.data_model_id).first()
                if not db_data_model:
                    raise Exception(f"数据模型不存在: {chart_update.data_model_id}")

            # 更新图表
            update_data = chart_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_chart, key, value)

            db.commit()
            db.refresh(db_chart)
            return db_chart
        finally:
            db.close()

    async def delete(self, chart_id: int) -> None:
        db = SessionLocal()
        try:
            db_chart = db.query(Chart).filter(Chart.id == chart_id).first()
            if not db_chart:
                raise Exception(f"图表不存在: {chart_id}")

            db.delete(db_chart)
            db.commit()
        finally:
            db.close()

class DashboardService:
    def __init__(self):
        pass

    async def create(self, dashboard: DashboardCreate) -> Dashboard:
        db = SessionLocal()
        try:
            # 验证图表是否存在
            for widget in dashboard.widgets:
                if widget.type == "chart" and widget.chart_id:
                    db_chart = db.query(Chart).filter(Chart.id == widget.chart_id).first()
                    if not db_chart:
                        raise Exception(f"图表不存在: {widget.chart_id}")

            # 创建仪表盘
            db_dashboard = Dashboard(
                name=dashboard.name,
                description=dashboard.description,
                layout=dashboard.layout.model_dump(),
                widgets=[widget.model_dump() for widget in dashboard.widgets],
                refresh_interval=dashboard.refresh_interval
            )
            db.add(db_dashboard)
            db.commit()
            db.refresh(db_dashboard)
            return db_dashboard
        finally:
            db.close()

    async def get_all(self) -> List[Dashboard]:
        db = SessionLocal()
        try:
            return db.query(Dashboard).all()
        finally:
            db.close()

    async def get_by_id(self, dashboard_id: int) -> Dashboard:
        db = SessionLocal()
        try:
            dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
            if not dashboard:
                raise Exception(f"仪表盘不存在: {dashboard_id}")
            return dashboard
        finally:
            db.close()

    async def update(self, dashboard_id: int, dashboard_update: DashboardUpdate) -> Dashboard:
        db = SessionLocal()
        try:
            # 获取现有仪表盘
            db_dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
            if not db_dashboard:
                raise Exception(f"仪表盘不存在: {dashboard_id}")

            # 验证图表是否存在
            if dashboard_update.widgets:
                for widget in dashboard_update.widgets:
                    if widget.type == "chart" and widget.chart_id:
                        db_chart = db.query(Chart).filter(Chart.id == widget.chart_id).first()
                        if not db_chart:
                            raise Exception(f"图表不存在: {widget.chart_id}")

            # 准备更新数据
            update_data = dashboard_update.model_dump(exclude_unset=True)

            # 处理嵌套模型
            if "layout" in update_data:
                update_data["layout"] = update_data["layout"].model_dump()
            if "widgets" in update_data:
                update_data["widgets"] = [widget.model_dump() for widget in update_data["widgets"]]

            # 更新仪表盘
            for key, value in update_data.items():
                setattr(db_dashboard, key, value)

            db.commit()
            db.refresh(db_dashboard)
            return db_dashboard
        finally:
            db.close()

    async def delete(self, dashboard_id: int) -> None:
        db = SessionLocal()
        try:
            db_dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
            if not db_dashboard:
                raise Exception(f"仪表盘不存在: {dashboard_id}")

            db.delete(db_dashboard)
            db.commit()
        finally:
            db.close()

chart_service = ChartService()
dashboard_service = DashboardService()
