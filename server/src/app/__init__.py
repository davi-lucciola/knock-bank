from fastapi import FastAPI, HTTPException, Request, status
from typing import Callable
from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app import routes

from core.log import logger
from core.config import settings
from utils.schemas import MessageResponse


@asynccontextmanager
async def default_lifespan(app: FastAPI):
    """Initialize application services."""
    # Process Like Consumers and CronJobs
    yield
    # Finishing that Process


def create_app(lifespan: Callable = default_lifespan) -> FastAPI:
    """Creating FastAPI application."""
    app = FastAPI(
        title=settings.API_TITLE, description=settings.DESCRIPTION, lifespan=lifespan
    )

    routes.init_routes(app)

    @app.exception_handler(Exception)
    def generic_exception_handler(request: Request, exc: Exception):
        logger.error(exc)
        content = MessageResponse(
            message='Houve um error ao processar sua solicitação.'
        ).model_dump()
        return JSONResponse(content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request: Request, exc: RequestValidationError):
        details = []

        for content in exc.args[0]:
            detail = {content.get('type'): content.get('msg')}

            if content.get('type') == 'value_error':
                detail.update(
                    {'value_error': content.get('msg').replace('Value error, ', '')}
                )

            details.append(detail)

        content = MessageResponse(
            message='Validation Error', detail=details
        ).model_dump()
        return JSONResponse(content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        content = MessageResponse(message=exc.detail).model_dump()
        return JSONResponse(content, status_code=exc.status_code)

    return app
