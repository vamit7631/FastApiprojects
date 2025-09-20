from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.core.constants import StatusCodes, Messages
from app.core.logger import error_logger, warning_logger


class AuthError(HTTPException):
    """Custom exception for authentication errors."""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=StatusCodes.UNAUTHORIZED, detail=detail)


async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all for unhandled exceptions."""
    error_logger.exception(f"Unhandled exception at {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=StatusCodes.SERVER_ERROR,
        content={
            "detail": f"{Messages.SERVER_ERROR}: {str(exc)}",
        },
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handles duplicate entry / constraint errors."""
    warning_logger.warning(f"Database integrity error at {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=StatusCodes.CONFLICT,
        content={
            "detail": f"{Messages.CONFLICT}: {str(exc)}",
        },
    )


async def auth_error_handler(request: Request, exc: AuthError):
    """Handles authentication/authorization errors."""
    warning_logger.warning(f"Authentication failed at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles all FastAPI HTTPExceptions."""
    warning_logger.warning(f"HTTPException at {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        },
    )
