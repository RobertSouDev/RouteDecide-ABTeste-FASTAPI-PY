"""Serviço de lógica de negócio para testes."""
from typing import Dict, List

from repositories.test_repository import TestRepository
from services.variant_selector import VariantSelector
from core.exceptions import (
    InvalidDistributionError, 
    TestNotFoundError, 
    TestInactiveError,
    TestAlreadyExistsError
)
from schemas.models import ExperimentResponse, Section


class TestService:
    """Serviço para gerenciar testes e experimentos."""
    
    def __init__(self, repository: TestRepository, variant_selector: VariantSelector):
        self.repository = repository
        self.variant_selector = variant_selector
    
    def validate_distribution(self, variants: List[Dict]) -> None:
        """
        Valida que a soma das distribuições é 100.
        
        Raises:
            InvalidDistributionError: Se a soma não for 100
        """
        total_distribution = sum(v["distribution"] for v in variants)
        if abs(total_distribution - 100) > 0.01:  # Permitir pequena diferença de ponto flutuante
            raise InvalidDistributionError(
                f"Total distribution must equal 100, got {total_distribution}"
            )
    
    def create_test(
        self,
        test_id: str,
        name: str,
        variants: List[Dict]
    ) -> str:
        """
        Cria ou atualiza um teste.
        
        Args:
            test_id: ID do teste
            name: Nome do teste
            variants: Lista de variantes
            
        Returns:
            Mensagem indicando que foi criado
            
        Raises:
            TestAlreadyExistsError: Se o teste já existir
            InvalidDistributionError: Se a distribuição for inválida
        """
        # Validar distribuição
        self.validate_distribution(variants)
        
        # Verificar se o teste já existe
        existing_test = self.repository.get_test(test_id)
        
        if existing_test:
            raise TestAlreadyExistsError(f"Test {test_id} already exists")

        # Criar novo
        self.repository.save_test(test_id, name, variants, "active")
        return "Test created"
    
    def update_test(
        self,
        test_id: str,
        name: str,
        variants: List[Dict]
    ) -> str:
        """
        Atualiza um teste existente.
        
        Args:
            test_id: ID do teste
            name: Nome do teste
            variants: Lista de variantes
            
        Returns:
            Mensagem indicando que foi atualizado
            
        Raises:
            TestNotFoundError: Se o teste não existir
            InvalidDistributionError: Se a distribuição for inválida
        """
        # Validar distribuição
        self.validate_distribution(variants)
        
        # Verificar se o teste existe
        existing_test = self.repository.get_test(test_id)
        
        if not existing_test:
            raise TestNotFoundError(f"Test {test_id} not found")
        
        # Atualizar mantendo o status atual
        self.repository.save_test(
            test_id, 
            name, 
            variants, 
            existing_test["status"]
        )
        return "Test updated"
    
    def get_experiment(self, test_id: str) -> ExperimentResponse:
        """
        Obtém a variante e registra impressão.
        
        Args:
            test_id: ID do teste
            
        Returns:
            Resposta com variante e seções
            
        Raises:
            TestNotFoundError: Se o teste não existir
            TestInactiveError: Se o teste estiver inativo
        """
        # Buscar o teste ativo
        test = self.repository.get_active_test_or_raise(test_id)
        
        # Selecionar variante baseada na distribuição
        selected_variant = self.variant_selector.select_variant(
            test["variants"], 
            test_id
        )
        
        # Registrar impressão
        self.repository.add_impression(
            test_id, 
            selected_variant["variantId"]
        )
        
        # Retornar seções
        sections = [Section(**section) for section in selected_variant["sections"]]
        
        return ExperimentResponse(
            variantId=selected_variant["variantId"],
            sections=sections
        )
    
    def register_conversion(
        self,
        test_id: str,
        variant_id: str,
        event: str
    ) -> None:
        """
        Registra uma conversão.
        
        Args:
            test_id: ID do teste
            variant_id: ID da variante
            event: Tipo de evento
            
        Raises:
            TestNotFoundError: Se o teste não existir
        """
        # Verificar se o teste existe
        self.repository.get_test_or_raise(test_id)
        
        # Registrar conversão
        self.repository.add_conversion(test_id, variant_id, event)

