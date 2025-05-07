from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.log import logger
from app.auth.router import auth_router
from app.account.router import account_router
from app.transaction.router import transaction_router
from utils.schemas import MessageResponse


def init_routes(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:3000'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(auth_router)
    app.include_router(account_router)
    app.include_router(transaction_router)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    def generic_exception_handler(request: Request, exc: Exception):
        logger.error(exc)
        content = MessageResponse(message='Houve um error ao processar sua solicitação.')
        return JSONResponse(content.model_dump(mode='json'), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        content = MessageResponse(message='Validation error', detail=details)
        return JSONResponse(content.model_dump(mode='json'), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        content = MessageResponse(message=exc.detail).model_dump()
        return JSONResponse(content, status_code=exc.status_code)
