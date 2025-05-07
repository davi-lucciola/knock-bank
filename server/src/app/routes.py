from fastapi import FastAPI
from app.auth.router import auth_router
from app.account.router import account_router
from app.transaction.router import transaction_router
from fastapi.middleware.cors import CORSMiddleware


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
