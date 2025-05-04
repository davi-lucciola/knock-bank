from knockbankapi.domain.services import AuthService, AccountService, TransactionService
from knockbankapi.infra.db import db
from knockbankapi.infra.utils import JwtService
from knockbankapi.infra.repositories import (
    TransactionRepository,
    AccountRepository,
    UserRepository,
)


def get_account_service() -> AccountService:
    account_repository = AccountRepository(db)
    transaction_repository = TransactionRepository(db)

    account_service: AccountService = AccountService(
        account_repository, transaction_repository
    )
    return account_service


def get_auth_service() -> AuthService:
    jwt_service = JwtService()
    user_repository = UserRepository(db)
    account_repository = AccountRepository(db)

    auth_service = AuthService(jwt_service, user_repository, account_repository)
    return auth_service


def get_transaction_service() -> TransactionService:
    account_repository = AccountRepository(db)
    transaction_repository = TransactionRepository(db)

    return TransactionService(account_repository, transaction_repository)
