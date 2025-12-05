"""Rotas administrativas."""
from fastapi import APIRouter, Depends

from schemas.models import (
    AdminTestRequest,
    AdminTestUpdateRequest,
    AdminTestResponse,
    TestMetricsResponse,
    TestsListResponse,
    TestListItem,
)
from services.test_service import TestService
from services.metrics_service import MetricsService
from repositories.test_repository import TestRepository
from api.dependencies import get_test_service, get_metrics_service, get_repository

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/test", response_model=AdminTestResponse)
def create_test(
    request: AdminTestRequest,
    test_service: TestService = Depends(get_test_service)
):
    """
    Cria um novo experimento.
    """
    # Preparar variantes
    variants_dict = [
        {
            "variantId": v.variantId,
            "distribution": v.distribution,
            "sections": [s.dict() for s in v.sections]
        }
        for v in request.variants
    ]
    
    message = test_service.create_test(
        request.testId,
        request.name,
        variants_dict
    )
    
    return AdminTestResponse(ok=True, message=message)


@router.put("/test/{test_id}", response_model=AdminTestResponse)
def update_test(
    test_id: str,
    request: AdminTestUpdateRequest,
    test_service: TestService = Depends(get_test_service)
):
    """
    Atualiza um experimento existente.
    """
    # Preparar variantes
    variants_dict = [
        {
            "variantId": v.variantId,
            "distribution": v.distribution,
            "sections": [s.dict() for s in v.sections]
        }
        for v in request.variants
    ]
    
    message = test_service.update_test(
        test_id,
        request.name,
        variants_dict
    )
    
    return AdminTestResponse(ok=True, message=message)


@router.get("/test/{test_id}/metrics", response_model=TestMetricsResponse)
def get_test_metrics(
    test_id: str,
    metrics_service: MetricsService = Depends(get_metrics_service)
):
    """
    Retorna as métricas de cada variante do teste.
    """
    return metrics_service.get_test_metrics(test_id)


@router.get("/tests", response_model=TestsListResponse)
def list_tests(repository: TestRepository = Depends(get_repository)):
    """
    Lista todos os testes cadastrados.
    """
    all_tests = repository.get_all_tests()
    
    test_items = [
        TestListItem(
            testId=test["testId"],
            name=test["name"],
            status=test["status"],
            variantCount=len(test["variants"])
        )
        for test in all_tests
    ]
    
    return TestsListResponse(tests=test_items)

