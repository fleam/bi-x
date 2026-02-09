from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.data_models import DataSet, DataModel
from app.schemas.data_models import DataSetCreate, DataSetUpdate, DataModelCreate, DataModelUpdate
from app.core.database import SessionLocal

class DataSetService:
    def __init__(self):
        pass

    async def create(self, data_set: DataSetCreate) -> DataSet:
        db = SessionLocal()
        try:
            # 验证数据源是否存在
            from app.models.sources import DataSource
            db_data_source = db.query(DataSource).filter(DataSource.id == data_set.data_source_id).first()
            if not db_data_source:
                raise Exception(f"数据源不存在: {data_set.data_source_id}")

            # 创建数据集
            db_data_set = DataSet(**data_set.model_dump())
            db.add(db_data_set)
            db.commit()
            db.refresh(db_data_set)
            return db_data_set
        finally:
            db.close()

    async def get_all(self) -> List[DataSet]:
        db = SessionLocal()
        try:
            return db.query(DataSet).all()
        finally:
            db.close()

    async def get_by_id(self, data_set_id: int) -> DataSet:
        db = SessionLocal()
        try:
            data_set = db.query(DataSet).filter(DataSet.id == data_set_id).first()
            if not data_set:
                raise Exception(f"数据集不存在: {data_set_id}")
            return data_set
        finally:
            db.close()

    async def update(self, data_set_id: int, data_set_update: DataSetUpdate) -> DataSet:
        db = SessionLocal()
        try:
            # 获取现有数据集
            db_data_set = db.query(DataSet).filter(DataSet.id == data_set_id).first()
            if not db_data_set:
                raise Exception(f"数据集不存在: {data_set_id}")

            # 验证数据源是否存在
            if data_set_update.data_source_id:
                from app.models.sources import DataSource
                db_data_source = db.query(DataSource).filter(DataSource.id == data_set_update.data_source_id).first()
                if not db_data_source:
                    raise Exception(f"数据源不存在: {data_set_update.data_source_id}")

            # 更新数据集
            update_data = data_set_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_data_set, key, value)

            db.commit()
            db.refresh(db_data_set)
            return db_data_set
        finally:
            db.close()

    async def delete(self, data_set_id: int) -> None:
        db = SessionLocal()
        try:
            db_data_set = db.query(DataSet).filter(DataSet.id == data_set_id).first()
            if not db_data_set:
                raise Exception(f"数据集不存在: {data_set_id}")

            db.delete(db_data_set)
            db.commit()
        finally:
            db.close()

class DataModelService:
    def __init__(self):
        pass

    async def create(self, data_model: DataModelCreate) -> DataModel:
        db = SessionLocal()
        try:
            # 验证所有数据集是否存在
            for data_set_config in data_model.data_sets:
                db_data_set = db.query(DataSet).filter(DataSet.id == data_set_config.data_set_id).first()
                if not db_data_set:
                    raise Exception(f"数据集不存在: {data_set_config.data_set_id}")

            # 创建数据模型
            db_data_model = DataModel(**data_model.model_dump())
            db.add(db_data_model)
            db.commit()
            db.refresh(db_data_model)
            return db_data_model
        finally:
            db.close()

    async def get_all(self) -> List[DataModel]:
        db = SessionLocal()
        try:
            return db.query(DataModel).all()
        finally:
            db.close()

    async def get_by_id(self, data_model_id: int) -> DataModel:
        db = SessionLocal()
        try:
            data_model = db.query(DataModel).filter(DataModel.id == data_model_id).first()
            if not data_model:
                raise Exception(f"数据模型不存在: {data_model_id}")
            return data_model
        finally:
            db.close()

    async def update(self, data_model_id: int, data_model_update: DataModelUpdate) -> DataModel:
        db = SessionLocal()
        try:
            # 获取现有数据模型
            db_data_model = db.query(DataModel).filter(DataModel.id == data_model_id).first()
            if not db_data_model:
                raise Exception(f"数据模型不存在: {data_model_id}")

            # 验证所有数据集是否存在（如果更新了数据集列表）
            if data_model_update.data_sets:
                for data_set_config in data_model_update.data_sets:
                    db_data_set = db.query(DataSet).filter(DataSet.id == data_set_config.data_set_id).first()
                    if not db_data_set:
                        raise Exception(f"数据集不存在: {data_set_config.data_set_id}")

            # 更新数据模型
            update_data = data_model_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_data_model, key, value)

            db.commit()
            db.refresh(db_data_model)
            return db_data_model
        finally:
            db.close()

    async def delete(self, data_model_id: int) -> None:
        db = SessionLocal()
        try:
            db_data_model = db.query(DataModel).filter(DataModel.id == data_model_id).first()
            if not db_data_model:
                raise Exception(f"数据模型不存在: {data_model_id}")

            db.delete(db_data_model)
            db.commit()
        finally:
            db.close()

data_set_service = DataSetService()
data_model_service = DataModelService()
