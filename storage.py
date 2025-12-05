"""
Armazenamento em memória para testes, impressões e conversões.
"""
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


# Estruturas de dados em memória
tests: Dict[str, dict] = {}
impressions: List[dict] = []
conversions: List[dict] = []


def get_test(test_id: str) -> Optional[dict]:
    """Busca um teste pelo ID"""
    return tests.get(test_id)


def save_test(test_id: str, name: str, variants: list, status: str = "active"):
    """Salva ou atualiza um teste"""
    tests[test_id] = {
        "testId": test_id,
        "name": name,
        "variants": variants,
        "status": status
    }


def add_impression(test_id: str, variant_id: str):
    """Adiciona uma impressão"""
    impression = {
        "id": str(uuid4()),
        "testId": test_id,
        "variantId": variant_id,
        "timestamp": datetime.utcnow()
    }
    impressions.append(impression)
    return impression


def add_conversion(test_id: str, variant_id: str, event: str):
    """Adiciona uma conversão"""
    conversion = {
        "id": str(uuid4()),
        "testId": test_id,
        "variantId": variant_id,
        "event": event,
        "timestamp": datetime.utcnow()
    }
    conversions.append(conversion)
    return conversion


def count_impressions(test_id: str, variant_id: str) -> int:
    """Conta impressões para um teste e variante específicos"""
    return sum(
        1 for imp in impressions
        if imp["testId"] == test_id and imp["variantId"] == variant_id
    )


def count_conversions(test_id: str, variant_id: str) -> int:
    """Conta conversões para um teste e variante específicos"""
    return sum(
        1 for conv in conversions
        if conv["testId"] == test_id and conv["variantId"] == variant_id
    )


def get_all_tests() -> List[dict]:
    """Retorna todos os testes"""
    return list(tests.values())

