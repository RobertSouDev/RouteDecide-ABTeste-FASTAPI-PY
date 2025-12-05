"""Modelos Pydantic para validação de dados."""
from pydantic import BaseModel
from typing import List


class Section(BaseModel):
    id: str
    contentUrl: str


class Variant(BaseModel):
    variantId: str
    distribution: float
    sections: List[Section]


class Test(BaseModel):
    testId: str
    name: str
    variants: List[Variant]
    status: str = "active"


class ExperimentRequest(BaseModel):
    testId: str


class ExperimentResponse(BaseModel):
    variantId: str
    sections: List[Section]


class ConversionRequest(BaseModel):
    testId: str
    variantId: str
    event: str


class ConversionResponse(BaseModel):
    ok: bool = True


class AdminTestRequest(BaseModel):
    testId: str
    name: str
    variants: List[Variant]


class AdminTestUpdateRequest(BaseModel):
    name: str
    variants: List[Variant]


class AdminTestResponse(BaseModel):
    ok: bool = True
    message: str = "Test created"


class VariantMetrics(BaseModel):
    variantId: str
    impressions: int
    conversions: int
    conversionRate: float


class TestMetricsResponse(BaseModel):
    testId: str
    variants: List[VariantMetrics]


class TestListItem(BaseModel):
    testId: str
    name: str
    status: str
    variantCount: int


class TestsListResponse(BaseModel):
    tests: List[TestListItem]

