"""Exceções customizadas do sistema."""


class ABTestException(Exception):
    """Exceção base para erros do sistema A/B Testing."""
    pass


class TestNotFoundError(ABTestException):
    """Teste não encontrado."""
    pass


class TestInactiveError(ABTestException):
    """Teste está inativo."""
    pass


class InvalidDistributionError(ABTestException):
    """Distribuição de variantes inválida."""
    pass


class VisitorNotSeenVariantError(ABTestException):
    """Visitante não viu a variante especificada."""
    pass


class TestAlreadyExistsError(ABTestException):
    """Teste já existe."""
    pass

