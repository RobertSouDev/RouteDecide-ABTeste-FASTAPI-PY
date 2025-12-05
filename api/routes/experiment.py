"""Rotas de experimento."""
from fastapi import APIRouter, Depends, Query

from schemas.models import (
    ExperimentRequest,
    ExperimentResponse,
)
from services.test_service import TestService
from api.dependencies import get_test_service

router = APIRouter(tags=["experiment"])


@router.get("/experiment", response_model=ExperimentResponse)
def get_experiment_get(
    testId: str = Query(..., description="ID do teste"),
    test_service: TestService = Depends(get_test_service)
):
    """
    Retorna a variante a ser exibida e registra uma impressão.
    Aceita testId como query parameter.
    """
    return test_service.get_experiment(testId)


@router.post("/experiment", response_model=ExperimentResponse)
def get_experiment_post(
    request: ExperimentRequest,
    test_service: TestService = Depends(get_test_service)
):
    """
    Retorna a variante a ser exibida e registra uma impressão.
    Aceita JSON no body conforme documentação.
    """
    return test_service.get_experiment(request.testId)

