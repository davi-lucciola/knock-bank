from fastapi import Depends
from dataclasses import dataclass
from core import security
from app.auth.exceptions import *
from app.auth.models import User
from app.auth.schemas import TokenIn
from app.auth.repository import UserRepository
from app.account.repository import AccountRepository


@dataclass
class AuthService:
    user_repository: UserRepository = Depends(UserRepository)
    account_repository: AccountRepository = Depends(AccountRepository)

    def login(self, token_in: TokenIn) -> str:
        account = self.account_repository.get_by_cpf(token_in.cpf)

        invalid_credentials = (
            account is None
            or account.user.verify_password_hash(token_in.password) is False
        )

        if invalid_credentials:
            raise InvalidCredentials()

        if account is not None and account.fl_active is False:
            raise CantLoginInBlockedAccount()

        token: str = security.create_token(account.user_id)

        account.user.token = token
        self.account_repository.save(account)

        return token

    def logout(self, user: User) -> None:
        user.token, user.refresh_token = None, None
        self.user_repository.save(user)
