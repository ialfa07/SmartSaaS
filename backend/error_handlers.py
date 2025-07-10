
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from logger import logger
import traceback

async def validation_exception_handler(request: Request, exc):
    """Gestionnaire pour les erreurs de validation"""
    logger.error(f"Erreur de validation: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Données invalides",
            "details": str(exc),
            "path": str(request.url.path)
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Gestionnaire pour les erreurs HTTP"""
    logger.error(f"Erreur HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Gestionnaire pour toutes les autres erreurs"""
    error_id = f"ERR_{int(time.time())}"
    logger.error(f"Erreur interne [{error_id}]: {str(exc)}\n{traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erreur interne du serveur",
            "error_id": error_id,
            "message": "Une erreur inattendue s'est produite"
        }
    )
