from fastapi import APIRouter, HTTPException
from app.schemas.visualization import PivotAnalysisRequest, PivotAnalysisResponse, AdhocQueryRequest, AdhocQueryResponse, SpreadsheetRequest, SpreadsheetResponse
from app.services.visualization import visualization_service

router = APIRouter()

@router.post("/pivot-analysis", response_model=PivotAnalysisResponse)
async def pivot_analysis(request: PivotAnalysisRequest):
    try:
        return await visualization_service.pivot_analysis(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/adhoc-query", response_model=AdhocQueryResponse)
async def adhoc_query(request: AdhocQueryRequest):
    try:
        return await visualization_service.adhoc_query(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/spreadsheet", response_model=SpreadsheetResponse)
async def spreadsheet(request: SpreadsheetRequest):
    try:
        return await visualization_service.spreadsheet(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
