import asyncio
import mysql.connector
import oracledb
import psycopg2
import pandas as pd
import requests
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.sources import DataSource
from app.schemas.sources import DataSourceCreate, DataSourceUpdate, TestConnectionRequest
from app.core.config import settings
from app.core.database import SessionLocal

class DataSourceService:
    def __init__(self):
        pass

    async def create(self, data_source: DataSourceCreate) -> DataSource:
        db = SessionLocal()
        try:
            # 验证数据源连接
            test_request = TestConnectionRequest(**data_source.model_dump())
            test_result = await self.test_connection(test_request)
            if not test_result["success"]:
                raise Exception(f"连接测试失败: {test_result['message']}")

            # 创建数据源
            db_data_source = DataSource(**data_source.model_dump())
            db.add(db_data_source)
            db.commit()
            db.refresh(db_data_source)
            return db_data_source
        finally:
            db.close()

    async def get_all(self) -> List[DataSource]:
        db = SessionLocal()
        try:
            result = db.execute(select(DataSource))
            return result.scalars().all()
        finally:
            db.close()

    async def get_by_id(self, source_id: int) -> DataSource:
        db = SessionLocal()
        try:
            result = db.execute(select(DataSource).where(DataSource.id == source_id))
            data_source = result.scalars().first()
            if not data_source:
                raise Exception(f"数据源不存在: {source_id}")
            return data_source
        finally:
            db.close()

    async def update(self, source_id: int, data_source_update: DataSourceUpdate) -> DataSource:
        db = SessionLocal()
        try:
            # 获取现有数据源
            result = db.execute(select(DataSource).where(DataSource.id == source_id))
            db_data_source = result.scalars().first()
            if not db_data_source:
                raise Exception(f"数据源不存在: {source_id}")

            # 准备更新数据
            update_data = data_source_update.model_dump(exclude_unset=True)
            
            # 如果更新了连接信息，验证连接
            if any(key in update_data for key in ["host", "port", "database", "username", "password", "file_path", "api_url"]):
                # 构建测试请求
                test_data = {**db_data_source.__dict__, **update_data}
                test_request = TestConnectionRequest(**test_data)
                test_result = await self.test_connection(test_request)
                if not test_result["success"]:
                    raise Exception(f"连接测试失败: {test_result['message']}")

            # 更新数据源
            for key, value in update_data.items():
                setattr(db_data_source, key, value)

            db.commit()
            db.refresh(db_data_source)
            return db_data_source
        finally:
            db.close()

    async def delete(self, source_id: int) -> None:
        db = SessionLocal()
        try:
            result = db.execute(select(DataSource).where(DataSource.id == source_id))
            db_data_source = result.scalars().first()
            if not db_data_source:
                raise Exception(f"数据源不存在: {source_id}")

            db.delete(db_data_source)
            db.commit()
        finally:
            db.close()

    async def test_connection(self, request: TestConnectionRequest) -> dict:
        try:
            if request.type == "database":
                return await self._test_database_connection(request)
            elif request.type == "excel":
                return await self._test_excel_connection(request)
            elif request.type == "api":
                return await self._test_api_connection(request)
            else:
                return {"success": False, "message": f"不支持的数据源类型: {request.type}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def _test_database_connection(self, request: TestConnectionRequest) -> dict:
        if not request.db_type:
            return {"success": False, "message": "数据库类型不能为空"}

        try:
            if request.db_type == "mysql":
                conn = mysql.connector.connect(
                    host=request.host,
                    port=request.port,
                    user=request.username,
                    password=request.password,
                    database=request.database
                )
                conn.close()
            elif request.db_type == "oracle":
                conn = oracledb.connect(
                    user=request.username,
                    password=request.password,
                    dsn=f"{request.host}:{request.port}/{request.database}"
                )
                conn.close()
            elif request.db_type == "postgresql":
                conn = psycopg2.connect(
                    host=request.host,
                    port=request.port,
                    database=request.database,
                    user=request.username,
                    password=request.password
                )
                conn.close()
            else:
                return {"success": False, "message": f"不支持的数据库类型: {request.db_type}"}
            return {"success": True, "message": "连接成功"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def _test_excel_connection(self, request: TestConnectionRequest) -> dict:
        if not request.file_path:
            return {"success": False, "message": "文件路径不能为空"}

        try:
            # 尝试读取Excel文件的前几行
            df = pd.read_excel(request.file_path, nrows=5)
            return {"success": True, "message": f"文件读取成功，包含 {len(df.columns)} 列"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def _test_api_connection(self, request: TestConnectionRequest) -> dict:
        if not request.api_url:
            return {"success": False, "message": "API地址不能为空"}

        try:
            method = request.api_method or "get"
            headers = request.api_headers or {}
            data = request.api_body or {}

            if method.lower() == "get":
                response = requests.get(request.api_url, headers=headers, params=data, timeout=10)
            else:
                response = requests.post(request.api_url, headers=headers, json=data, timeout=10)

            response.raise_for_status()
            return {"success": True, "message": f"API请求成功，状态码: {response.status_code}"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def get_tables(self, source_id: int) -> List[str]:
        """获取数据源下的表列表"""
        try:
            # 获取数据源信息
            data_source = await self.get_by_id(source_id)
            
            # 根据数据源类型返回不同的表列表
            if data_source.type == "database":
                if data_source.db_type == "mysql":
                    conn = mysql.connector.connect(
                        host=data_source.host,
                        port=data_source.port,
                        user=data_source.username,
                        password=data_source.password,
                        database=data_source.database
                    )
                    cursor = conn.cursor()
                    cursor.execute("SHOW TABLES")
                    tables = [table[0] for table in cursor.fetchall()]
                    cursor.close()
                    conn.close()
                    return tables
                elif data_source.db_type == "postgresql":
                    conn = psycopg2.connect(
                        host=data_source.host,
                        port=data_source.port,
                        database=data_source.database,
                        user=data_source.username,
                        password=data_source.password
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                    tables = [table[0] for table in cursor.fetchall()]
                    cursor.close()
                    conn.close()
                    return tables
                elif data_source.db_type == "oracle":
                    conn = oracledb.connect(
                        user=data_source.username,
                        password=data_source.password,
                        dsn=f"{data_source.host}:{data_source.port}/{data_source.database}"
                    )
                    cursor = conn.cursor()
                    cursor.execute("SELECT table_name FROM user_tables")
                    tables = [table[0] for table in cursor.fetchall()]
                    cursor.close()
                    conn.close()
                    return tables
            elif data_source.type == "excel":
                # Excel文件作为单个表处理
                return ["Sheet1"]
            elif data_source.type == "api":
                # API数据源作为单个表处理
                return ["API Data"]
            
            return []
        except Exception as e:
            print(f"获取表列表失败: {e}")
            return []

    async def get_fields(self, source_id: int, table_name: str) -> List[str]:
        """获取表的字段列表"""
        try:
            # 获取数据源信息
            data_source = await self.get_by_id(source_id)
            
            # 根据数据源类型返回不同的字段列表
            if data_source.type == "database":
                if data_source.db_type == "mysql":
                    conn = mysql.connector.connect(
                        host=data_source.host,
                        port=data_source.port,
                        user=data_source.username,
                        password=data_source.password,
                        database=data_source.database
                    )
                    cursor = conn.cursor()
                    cursor.execute(f"DESCRIBE {table_name}")
                    fields = [field[0] for field in cursor.fetchall()]
                    cursor.close()
                    conn.close()
                    return fields
                elif data_source.db_type == "postgresql":
                    conn = psycopg2.connect(
                        host=data_source.host,
                        port=data_source.port,
                        database=data_source.database,
                        user=data_source.username,
                        password=data_source.password
                    )
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
                    fields = [field[0] for field in cursor.fetchall()]
                    cursor.close()
                    conn.close()
                    return fields
                elif data_source.db_type == "oracle":
                    conn = oracledb.connect(
                        user=data_source.username,
                        password=data_source.password,
                        dsn=f"{data_source.host}:{data_source.port}/{data_source.database}"
                    )
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name.upper()}'")
                    fields = [field[0] for field in cursor.fetchall()]
                    cursor.close()
                    conn.close()
                    return fields
            elif data_source.type == "excel":
                # 读取Excel文件的列名
                df = pd.read_excel(data_source.file_path, nrows=0)
                return list(df.columns)
            elif data_source.type == "api":
                # 模拟API字段
                return ["field1", "field2", "field3"]
            
            return []
        except Exception as e:
            print(f"获取字段列表失败: {e}")
            return []
