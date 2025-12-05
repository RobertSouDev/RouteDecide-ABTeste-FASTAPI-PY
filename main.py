"""Aplicação FastAPI principal."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from core.config import settings
from core.exceptions import (
    ABTestException,
    TestNotFoundError,
    TestInactiveError,
    InvalidDistributionError,
    TestAlreadyExistsError,
)
from api.routes import admin, experiment, conversion

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION
)

# Configurar CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# Handler global de exceções
@app.exception_handler(ABTestException)
async def abtest_exception_handler(request: Request, exc: ABTestException):
    """Converte exceções customizadas em HTTPException."""
    if isinstance(exc, TestNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )
    elif isinstance(exc, TestInactiveError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )
    elif isinstance(exc, InvalidDistributionError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
    elif isinstance(exc, TestAlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


# Registrar rotas
app.include_router(admin.router)
app.include_router(experiment.router)
app.include_router(conversion.router)


@app.get("/")
def root():
    """Endpoint raiz."""
    return {
        "message": settings.API_TITLE,
        "docs": "/docs"
    }
