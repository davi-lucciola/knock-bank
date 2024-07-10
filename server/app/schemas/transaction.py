from apiflask import Schema
from typing import TypedDict
from apiflask.validators import OneOf
from datetime import datetime as dt, date
from marshmallow import validates, ValidationError
from app.schemas import TPaginationQuery, PaginationQuery, PersonOut
from apiflask.fields import Float, Integer, Nested, DateTime, Date, String


class TransactionQuery(PaginationQuery):
    transactionDate: date = Date()
    transactionType: int = Integer(
        validate=[
            OneOf([1, 2, None], error="Tipo de transação inválida, deve ser 1 ou 2.")
        ],
    )


class TTransactionQuery(TPaginationQuery):
    pageSize: int
    pageIndex: int
    transactionDate: date
    transactionType: int


class TransactionIn(Schema):
    money: float = Float(required=True)

    @validates("money")
    def validate_money(self, money: float, **kwargs):
        if money <= 0:
            raise ValidationError("O valor da transação deve ser maior que zero.")


class TransactionTransfer(TransactionIn):
    accountId: int = Integer(required=True)


class TransactionOut(Schema):
    id: int = Integer()
    money: float = Float()
    dateTime: dt = DateTime()
    transactionType: int = Integer()
    account: dict = Nested(PersonOut)
    originAccount: dict = Nested(PersonOut)


class TransactionMonthResume(Schema):
    month: str = String()
    label: str = String()
    amount: float = Float()


class TTransactionMonthResume(TypedDict):
    month: int
    label: str
    amount: float
