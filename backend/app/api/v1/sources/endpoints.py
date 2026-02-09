from fastapi import APIRouter, HTTPException
from app.schemas.sources import DataSourceCreate, DataSourceUpdate, DataSourceResponse, TestConnectionRequest, TestConnectionResponse
from app.services.sources import data_source_service

router = APIRouter()

@router.post("/", response_model=DataSourceResponse)
async def create_data_source(data_source: DataSourceCreate):
    try:
        return await data_source_service.create(data_source)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[DataSourceResponse])
async def get_data_sources():
    try:
        return await data_source_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{source_id}", response_model=DataSourceResponse)
async def get_data_source(source_id: int):
    try:
        return await data_source_service.get_by_id(source_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{source_id}", response_model=DataSourceResponse)
async def update_data_source(source_id: int, data_source: DataSourceUpdate):
    try:
        return await data_source_service.update(source_id, data_source)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{source_id}")
async def delete_data_source(source_id: int):
    try:
        await data_source_service.delete(source_id)
        return {"message": "数据源删除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/test-connection", response_model=TestConnectionResponse)
async def test_connection(request: TestConnectionRequest):
    try:
        result = await data_source_service.test_connection(request)
        return TestConnectionResponse(success=result["success"], message=result["message"])
    except Exception as e:
        return TestConnectionResponse(success=False, message=str(e))

@router.get("/{source_id}/tables")
async def get_tables(source_id: int):
    try:
        tables = await data_source_service.get_tables(source_id)
        return tables
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{source_id}/fields/{table_name}")
async def get_fields(source_id: int, table_name: str):
    try:
        fields = await data_source_service.get_fields(source_id, table_name)
        return fields
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
