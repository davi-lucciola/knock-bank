from pydantic import BaseModel, Field
from datetime import datetime, date
from utils.schemas import PaginationQuery
from app.account.schemas import PersonBasicOut


class TransactionFilter(PaginationQuery):
    transactionDate: date | None = None
    transactionType: int | None = Field(ge=1, le=2, default=None)


class MoneyIn(BaseModel):
    money: float = Field(gt=0)


class TransactionIn(MoneyIn):
    accountId: int


class TransactionTransferIn(TransactionIn):
    senderAccountId: int


class TransactionOut(BaseModel):
    id: int
    money: float
    dateTime: datetime
    transactionType: int
    account: PersonBasicOut | None = None
    originAccount: PersonBasicOut | None = None


class TransactionMonthResumeNumericOut(BaseModel):
    month: int
    label: str
    amount: float


class TransactionMonthResumeOut(BaseModel):
    month: str
    label: str
    amount: float
