"""Repositório para acesso aos dados de testes, impressões e conversões."""
from typing import Dict, List, Optional
from datetime import datetime
from uuid import uuid4

import storage
from core.exceptions import TestNotFoundError, TestInactiveError


class TestRepository:
    """Repositório para gerenciar testes, impressões e conversões."""
    
    def get_test(self, test_id: str) -> Optional[Dict]:
        """Busca um teste pelo ID."""
        return storage.get_test(test_id)
    
    def get_test_or_raise(self, test_id: str) -> Dict:
        """Busca um teste pelo ID ou levanta exceção se não encontrado."""
        test = self.get_test(test_id)
        if not test:
            raise TestNotFoundError(f"Test {test_id} not found")
        return test
    
    def get_active_test_or_raise(self, test_id: str) -> Dict:
        """Busca um teste ativo pelo ID ou levanta exceção."""
        test = self.get_test_or_raise(test_id)
        if test["status"] != "active":
            raise TestInactiveError(f"Test {test_id} is not active")
        return test
    
    def save_test(
        self, 
        test_id: str, 
        name: str, 
        variants: List[Dict], 
        status: str = "active"
    ) -> None:
        """Salva ou atualiza um teste."""
        storage.save_test(test_id, name, variants, status)
    
    def get_all_tests(self) -> List[Dict]:
        """Retorna todos os testes."""
        return storage.get_all_tests()
    
    def add_impression(
        self, 
        test_id: str, 
        variant_id: str
    ) -> Dict:
        """Adiciona uma impressão."""
        return storage.add_impression(test_id, variant_id)
    
    def add_conversion(
        self,
        test_id: str,
        variant_id: str,
        event: str
    ) -> Dict:
        """Adiciona uma conversão."""
        return storage.add_conversion(test_id, variant_id, event)
    
    def count_impressions(self, test_id: str, variant_id: str) -> int:
        """Conta impressões para um teste e variante específicos."""
        return storage.count_impressions(test_id, variant_id)
    
    def count_conversions(self, test_id: str, variant_id: str) -> int:
        """Conta conversões para um teste e variante específicos."""
        return storage.count_conversions(test_id, variant_id)

