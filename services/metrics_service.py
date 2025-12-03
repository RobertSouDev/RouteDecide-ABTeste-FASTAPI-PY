"""Serviço para cálculo de métricas."""
from typing import Dict, List

from repositories.test_repository import TestRepository
from schemas.models import TestMetricsResponse, VariantMetrics
from core.exceptions import TestNotFoundError


class MetricsService:
    """Serviço para calcular métricas de testes."""
    
    def __init__(self, repository: TestRepository):
        self.repository = repository
    
    def get_test_metrics(self, test_id: str) -> TestMetricsResponse:
        """
        Retorna as métricas de cada variante do teste.
        
        Args:
            test_id: ID do teste
            
        Returns:
            Métricas do teste com todas as variantes
            
        Raises:
            TestNotFoundError: Se o teste não existir
        """
        test = self.repository.get_test_or_raise(test_id)
        
        variants_metrics = []
        for variant in test["variants"]:
            variant_id = variant["variantId"]
            impressions_count = self.repository.count_impressions(test_id, variant_id)
            conversions_count = self.repository.count_conversions(test_id, variant_id)
            conversion_rate = (
                conversions_count / impressions_count 
                if impressions_count > 0 
                else 0.0
            )
            
            variants_metrics.append(
                VariantMetrics(
                    variantId=variant_id,
                    impressions=impressions_count,
                    conversions=conversions_count,
                    conversionRate=round(conversion_rate, 3)
                )
            )
        
        return TestMetricsResponse(
            testId=test_id,
            variants=variants_metrics
        )

