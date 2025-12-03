"""Serviço para seleção determinística de variantes."""
import hashlib
from typing import Dict, List


class VariantSelector:
    """Seleciona variantes baseado em hash determinístico."""
    
    @staticmethod
    def select_variant(variants: List[Dict], visitor_id: str, test_id: str) -> Dict:
        """
        Seleciona uma variante baseada na distribuição usando hash determinístico.
        O mesmo visitante sempre verá a mesma variante para garantir consistência no teste A/B.
        
        Args:
            variants: Lista de variantes com distribuição
            visitor_id: ID do visitante
            test_id: ID do teste
            
        Returns:
            Variante selecionada
        """
        # Criar hash determinístico baseado em test_id + visitor_id
        hash_input = f"{test_id}:{visitor_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        # Gerar valor entre 0 e 100 baseado no hash
        hash_percentage = (hash_value % 10000) / 100.0
        
        cumulative = 0
        for variant in variants:
            cumulative += variant["distribution"]
            if hash_percentage <= cumulative:
                return variant
        
        # Fallback para última variante
        return variants[-1]

