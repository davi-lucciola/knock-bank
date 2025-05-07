import math
from fastapi import Depends
from decimal import Decimal
from dataclasses import dataclass
from utils.schemas import PaginationResponse
from app.account.models import Account
from app.account.repository import AccountRepository
from app.transaction.exceptions import (
    CantTransferForYourself,
    DailyWithdrawLimitExceeded,
    InsuficientBalance,
    ReciverAccountNotFound,
    TransactionNotFound,
)
from app.transaction.schemas import (
    TransactionFilter,
    TransactionIn,
    TransactionOut,
    TransactionTransferIn,
)
from app.transaction.models import Transaction
from app.transaction.enums import TransactionType
from app.transaction.repository import TransactionRepository


@dataclass
class TransactionService:
    account_repository: AccountRepository = Depends(AccountRepository)
    transaction_repository: TransactionRepository = Depends(TransactionRepository)

    def get_all(
        self, filter: TransactionFilter, account_id: int
    ) -> PaginationResponse[TransactionOut]:
        transactions, total = self.transaction_repository.get_all(filter, account_id)
        transactions = [
            TransactionOut(**transaction.to_json()) for transaction in transactions
        ]

        return PaginationResponse(
            data=transactions,
            total=total,
            pageIndex=filter.pageIndex,
            pageSize=filter.pageSize,
            totalPages=math.ceil(total / filter.pageSize),
        )

    def get_month_transactions_resume(self, account_id: int):
        return self.transaction_repository.get_this_year_transactions(account_id)

    def get_by_id(self, transaction_id: int) -> Transaction:
        transaction = self.transaction_repository.get_by_id(transaction_id)

        if transaction is None:
            raise TransactionNotFound()

        return transaction

    def withdraw(self, transaction_in: TransactionIn):
        account: Account = self.account_repository.get_by_id(transaction_in.accountId)

        money: Decimal = Decimal(transaction_in.money)
        if account.balance - money < 0:
            raise InsuficientBalance()

        self.validate_daily_withdraw_limit(account, money)
        account.balance -= money

        transaction = Transaction(-money, TransactionType.WITHDRAW, account)
        self.transaction_repository.save(transaction)

    def deposit(self, transaction_in: TransactionIn):
        account: Account = self.account_repository.get_by_id(transaction_in.accountId)

        money: Decimal = Decimal(transaction_in.money)
        account.balance += money

        transaction = Transaction(money, TransactionType.DEPOSIT, account)
        self.transaction_repository.save(transaction)

    def transfer(self, transaction_transfer_in: TransactionTransferIn):
        sender_and_reciver_are_same_account = (
            transaction_transfer_in.accountId == transaction_transfer_in.senderAccountId
        )
        if sender_and_reciver_are_same_account:
            raise CantTransferForYourself()

        account_reciver = self.account_repository.get_by_id(
            transaction_transfer_in.accountId
        )

        if account_reciver is None:
            raise ReciverAccountNotFound('Conta destino não encontrada.')

        account_sender: Account = self.account_repository.get_by_id(
            transaction_transfer_in.senderAccountId
        )

        money: Decimal = Decimal(transaction_transfer_in.money)
        if account_sender.balance - money < 0:
            raise InsuficientBalance()

        self.validate_daily_withdraw_limit(account_sender, money)

        account_sender.balance -= money
        account_reciver.balance += money

        withdraw_transaction = Transaction(
            -money, TransactionType.WITHDRAW, account_sender, account_reciver
        )

        deposit_transaction = Transaction(
            money, TransactionType.DEPOSIT, account_reciver, account_sender
        )

        self.transaction_repository.save_all(
            [withdraw_transaction, deposit_transaction]
        )

    def validate_daily_withdraw_limit(self, account: Account, new_amount: Decimal):
        total = self.transaction_repository.get_total_today_withdraw(account.id)

        if round(-total + new_amount, 2) > account.daily_withdraw_limit:
            raise DailyWithdrawLimitExceeded()
