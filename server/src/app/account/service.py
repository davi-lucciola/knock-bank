import math
from fastapi import Depends
from datetime import date
from dataclasses import dataclass
from utils.schemas import PaginationResponse
from app.account.exceptions import *
from app.account.models import Account
from app.account.schemas import AccountOut, AccountFilter, AccountIn, UpdateAccountIn
from app.account.repository import AccountRepository
from app.transaction.repository import TransactionRepository


@dataclass
class AccountService:
    account_repository: AccountRepository = Depends(AccountRepository)
    transaction_repository: TransactionRepository = Depends(TransactionRepository)

    def get_all(
        self, filter: AccountFilter, account_id: int
    ) -> PaginationResponse[AccountOut]:
        accounts, total = self.account_repository.get_all(filter, account_id)
        accounts = [
            AccountOut(**account.to_json(mask_cpf=True)) for account in accounts
        ]

        return PaginationResponse(
            data=accounts,
            total=total,
            pageIndex=filter.pageIndex,
            pageSize=filter.pageSize,
            totalPages=math.ceil(total / filter.pageSize),
        )

    def get_by_id(self, account_id: int):
        account = self.account_repository.get_by_id(account_id)

        if account is None:
            raise AccountNotFound()

        return account

    def create(self, account_in: AccountIn):
        person_age = (date.today() - account_in.birthDate).days // 365

        if person_age < 18:
            raise AccountOwnerIsMinor()

        account = self.account_repository.get_by_cpf(account_in.cpf, True)

        if account is not None:
            raise AccountAlreadyExistsWithThisCPF()

        account = Account(**account_in.model_dump())
        return self.account_repository.save(account)

    def update(self, account_id: int, update_account_in: UpdateAccountIn, user_id: int):
        account: Account = self.get_by_id(account_id)

        if account.user_id != user_id:
            raise CantUpdateAccount()

        today_total_withdraw = float(
            -self.transaction_repository.get_total_today_withdraw(account.id)
        )

        if update_account_in.dailyWithdrawLimit < float(today_total_withdraw):
            raise CantUpdateDailyWithdrawLimit()

        account.update(update_account_in)
        return self.account_repository.save(account)

    def deactivate(self, account_id: int, user_id: int):
        account: Account = self.account_repository.get_by_id(account_id)

        if account.user_id != user_id:
            raise CantBlockAccount()

        account.fl_active = False
        account.user.token = None
        self.account_repository.save(account)
