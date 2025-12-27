# app/errors.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger("uvicorn.error")


def register_exception_handlers(app):
    """
    Register global exception handlers to return JSON responses.
    Call this from app.main after creating the FastAPI() instance.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        # You can customize the body here
        logger.info(f"HTTPException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Return a friendly validation error structure
        logger.info("Validation error: %s", exc.errors())
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # Log unexpected exceptions and return 500
        logger.exception("Unhandled exception occurred")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
