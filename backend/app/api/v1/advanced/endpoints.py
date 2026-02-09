from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from app.schemas.advanced import (
    AIAnalysisCreate, AIAnalysisUpdate, AIAnalysisResponse,
    PredictionModelCreate, PredictionModelUpdate, PredictionModelResponse,
    MacroCreate, MacroUpdate, MacroResponse,
    SystemMonitorCreate, SystemMonitorResponse,
    IntegrationCreate, IntegrationUpdate, IntegrationResponse
)
from app.services.advanced import (
    ai_analysis_service, prediction_model_service, macro_service, 
    system_monitor_service, integration_service
)
from app.schemas.permissions import UserResponse
from app.api.v1.permissions.endpoints import get_current_user

router = APIRouter()

# AI分析相关端点
@router.post("/ai-analyses", response_model=AIAnalysisResponse)
async def create_ai_analysis(
    analysis: AIAnalysisCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await ai_analysis_service.create(analysis, current_user.id)

@router.get("/ai-analyses", response_model=List[AIAnalysisResponse])
async def get_ai_analyses(current_user: UserResponse = Depends(get_current_user)):
    return await ai_analysis_service.get_all()

@router.get("/ai-analyses/{analysis_id}", response_model=AIAnalysisResponse)
async def get_ai_analysis(
    analysis_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return await ai_analysis_service.get_by_id(analysis_id)

@router.put("/ai-analyses/{analysis_id}", response_model=AIAnalysisResponse)
async def update_ai_analysis(
    analysis_id: int,
    analysis_update: AIAnalysisUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await ai_analysis_service.update(analysis_id, analysis_update)

@router.delete("/ai-analyses/{analysis_id}")
async def delete_ai_analysis(
    analysis_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    await ai_analysis_service.delete(analysis_id)
    return {"message": "AI分析删除成功"}

@router.post("/ai-analyses/{analysis_id}/run", response_model=AIAnalysisResponse)
async def run_ai_analysis(
    analysis_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return await ai_analysis_service.run_analysis(analysis_id)

# 预测模型相关端点
@router.post("/prediction-models", response_model=PredictionModelResponse)
async def create_prediction_model(
    model: PredictionModelCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await prediction_model_service.create(model, current_user.id)

@router.get("/prediction-models", response_model=List[PredictionModelResponse])
async def get_prediction_models(current_user: UserResponse = Depends(get_current_user)):
    return await prediction_model_service.get_all()

@router.get("/prediction-models/{model_id}", response_model=PredictionModelResponse)
async def get_prediction_model(
    model_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return await prediction_model_service.get_by_id(model_id)

@router.put("/prediction-models/{model_id}", response_model=PredictionModelResponse)
async def update_prediction_model(
    model_id: int,
    model_update: PredictionModelUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await prediction_model_service.update(model_id, model_update)

@router.delete("/prediction-models/{model_id}")
async def delete_prediction_model(
    model_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    await prediction_model_service.delete(model_id)
    return {"message": "预测模型删除成功"}

@router.post("/prediction-models/{model_id}/train", response_model=PredictionModelResponse)
async def train_prediction_model(
    model_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return await prediction_model_service.train_model(model_id)

# 宏相关端点
@router.post("/macros", response_model=MacroResponse)
async def create_macro(
    macro: MacroCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await macro_service.create(macro, current_user.id)

@router.get("/macros", response_model=List[MacroResponse])
async def get_macros(current_user: UserResponse = Depends(get_current_user)):
    return await macro_service.get_all()

@router.get("/macros/{macro_id}", response_model=MacroResponse)
async def get_macro(
    macro_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return await macro_service.get_by_id(macro_id)

@router.put("/macros/{macro_id}", response_model=MacroResponse)
async def update_macro(
    macro_id: int,
    macro_update: MacroUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await macro_service.update(macro_id, macro_update)

@router.delete("/macros/{macro_id}")
async def delete_macro(
    macro_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    await macro_service.delete(macro_id)
    return {"message": "宏删除成功"}

@router.post("/macros/{macro_id}/execute", response_model=Dict[str, Any])
async def execute_macro(
    macro_id: int,
    params: Dict[str, Any],
    current_user: UserResponse = Depends(get_current_user)
):
    return await macro_service.execute_macro(macro_id, params)

# 系统监控相关端点
@router.post("/system-monitors", response_model=SystemMonitorResponse)
async def create_system_monitor(
    monitor: SystemMonitorCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await system_monitor_service.create(monitor)

@router.get("/system-monitors", response_model=List[SystemMonitorResponse])
async def get_system_monitors(
    component: Optional[str] = None,
    limit: int = 100
):
    return await system_monitor_service.get_all(component, limit)

@router.get("/system-monitors/{monitor_id}", response_model=SystemMonitorResponse)
async def get_system_monitor(
    monitor_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return await system_monitor_service.get_by_id(monitor_id)

# 集成相关端点
@router.post("/integrations", response_model=IntegrationResponse)
async def create_integration(
    integration: IntegrationCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await integration_service.create(integration)

@router.get("/integrations", response_model=List[IntegrationResponse])
async def get_integrations(current_user: UserResponse = Depends(get_current_user)):
    return await integration_service.get_all()

@router.get("/integrations/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    integration_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    return await integration_service.get_by_id(integration_id)

@router.put("/integrations/{integration_id}", response_model=IntegrationResponse)
async def update_integration(
    integration_id: int,
    integration_update: IntegrationUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    return await integration_service.update(integration_id, integration_update)

@router.delete("/integrations/{integration_id}")
async def delete_integration(
    integration_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    await integration_service.delete(integration_id)
    return {"message": "集成删除成功"}
