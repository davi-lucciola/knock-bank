from pytz import timezone
from decimal import Decimal
from datetime import datetime as dt
from core.db import BaseModel, Long
from app.account.models import Account
from app.transaction.enums import TransactionType
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, relationship


class Transaction(BaseModel):
    __tablename__ = 'transactions'

    id: Mapped[int] = Column(Long, primary_key=True, autoincrement=True)
    date_time: Mapped[dt] = Column(DateTime, nullable=False, default=dt.now)
    money: Mapped[Decimal] = Column(Numeric(10, 2), nullable=False)
    transaction_type: Mapped[int] = Column(Integer, nullable=False)

    account_id: Mapped[int] = Column(Long, ForeignKey('accounts.id'), nullable=False)
    account: Mapped['Account'] = relationship('Account', foreign_keys=[account_id])

    origin_account_id: Mapped[int] = Column(
        Long, ForeignKey('accounts.id'), nullable=True
    )
    origin_account: Mapped['Account'] = relationship(
        'Account', foreign_keys=[origin_account_id]
    )

    def __init__(
        self,
        money: float,
        transaction_type: TransactionType,
        account: Account,
        origin_account: Account = None,
    ) -> None:
        self.money = (
            Decimal(-abs(money))
            if transaction_type == TransactionType.WITHDRAW
            else Decimal(abs(money))
        )
        self.transaction_type = transaction_type.value[0]
        self.account_id = account.id
        self.account = account
        self.origin_account_id = (
            origin_account.id if origin_account is not None else None
        )
        self.origin_account = origin_account

    def __str__(self) -> str:
        return f'<Transaction - {self.account.person.name} | R${self.money:.2f}>'

    def to_json(self):
        return {
            'id': self.id,
            'money': float(self.money),
            'dateTime': self.date_time.astimezone(timezone('America/Sao_Paulo')),
            'transactionType': self.transaction_type,
            'account': {
                'id': self.account.id,
                'name': self.account.person.name,
            },
            'originAccount': (
                {
                    'id': self.origin_account.id,
                    'name': self.origin_account.person.name,
                }
                if self.origin_account is not None
                else None
            ),
        }
