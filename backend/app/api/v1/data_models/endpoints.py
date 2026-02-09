from fastapi import APIRouter, HTTPException
from app.schemas.data_models import DataSetCreate, DataSetUpdate, DataSetResponse, DataModelCreate, DataModelUpdate, DataModelResponse
from app.services.data_models import data_set_service, data_model_service

router = APIRouter()

# 数据集相关接口
@router.post("/data-sets", response_model=DataSetResponse)
async def create_data_set(data_set: DataSetCreate):
    try:
        return await data_set_service.create(data_set)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/data-sets", response_model=list[DataSetResponse])
async def get_data_sets():
    try:
        return await data_set_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data-sets/{data_set_id}", response_model=DataSetResponse)
async def get_data_set(data_set_id: int):
    try:
        return await data_set_service.get_by_id(data_set_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/data-sets/{data_set_id}", response_model=DataSetResponse)
async def update_data_set(data_set_id: int, data_set: DataSetUpdate):
    try:
        return await data_set_service.update(data_set_id, data_set)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/data-sets/{data_set_id}")
async def delete_data_set(data_set_id: int):
    try:
        await data_set_service.delete(data_set_id)
        return {"message": "数据集删除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 数据模型相关接口
@router.post("/data-models", response_model=DataModelResponse)
async def create_data_model(data_model: DataModelCreate):
    try:
        return await data_model_service.create(data_model)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/data-models", response_model=list[DataModelResponse])
async def get_data_models():
    try:
        return await data_model_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data-models/{data_model_id}", response_model=DataModelResponse)
async def get_data_model(data_model_id: int):
    try:
        return await data_model_service.get_by_id(data_model_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/data-models/{data_model_id}", response_model=DataModelResponse)
async def update_data_model(data_model_id: int, data_model: DataModelUpdate):
    try:
        return await data_model_service.update(data_model_id, data_model)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/data-models/{data_model_id}")
async def delete_data_model(data_model_id: int):
    try:
        await data_model_service.delete(data_model_id)
        return {"message": "数据模型删除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
