"""Dependências compartilhadas para injeção."""
from repositories.test_repository import TestRepository
from services.variant_selector import VariantSelector
from services.test_service import TestService
from services.metrics_service import MetricsService


# Instâncias singleton dos serviços
_repository = TestRepository()
_variant_selector = VariantSelector()
_test_service = TestService(_repository, _variant_selector)
_metrics_service = MetricsService(_repository)


def get_repository() -> TestRepository:
    """Retorna instância do repositório."""
    return _repository


def get_test_service() -> TestService:
    """Retorna instância do serviço de testes."""
    return _test_service


def get_metrics_service() -> MetricsService:
    """Retorna instância do serviço de métricas."""
    return _metrics_service

