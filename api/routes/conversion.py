"""Rotas de conversão."""
from fastapi import APIRouter, Depends

from schemas.models import (
    ConversionRequest,
    ConversionResponse,
)
from services.test_service import TestService
from api.dependencies import get_test_service

router = APIRouter(tags=["conversion"])


@router.post("/conversion", response_model=ConversionResponse)
def register_conversion(
    request: ConversionRequest,
    test_service: TestService = Depends(get_test_service)
):
    """
    Registra uma conversão.
    """
    test_service.register_conversion(
        request.testId,
        request.variantId,
        request.event
    )
    return ConversionResponse(ok=True)

