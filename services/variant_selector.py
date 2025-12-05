"""Serviço para seleção de variantes."""
import random
from typing import Dict, List


class VariantSelector:
    """Seleciona variantes baseado na distribuição."""
    
    @staticmethod
    def select_variant(variants: List[Dict], test_id: str) -> Dict:
        """
        Seleciona uma variante baseada na distribuição usando seleção aleatória.
        
        Args:
            variants: Lista de variantes com distribuição
            test_id: ID do teste (não usado, mantido para compatibilidade)
            
        Returns:
            Variante selecionada
        """
        # Gerar valor aleatório entre 0 e 100
        random_percentage = random.random() * 100
        
        cumulative = 0
        for variant in variants:
            cumulative += variant["distribution"]
            if random_percentage <= cumulative:
                return variant
        
        # Fallback para última variante
        return variants[-1]

