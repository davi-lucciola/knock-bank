from datetime import date
from utils import validators
from utils.schemas import PaginationQuery
from pydantic import BaseModel, Field, field_validator


class PersonBasicOut(BaseModel):
    id: int
    name: str
    cpf: str | None = None


class PersonOut(PersonBasicOut):
    birthDate: date


class UpdateAccountIn(BaseModel):
    name: str
    birthDate: date
    accountType: int
    dailyWithdrawLimit: float


class AccountFilter(PaginationQuery):
    search: str | None = None


class AccountIn(BaseModel):
    name: str
    cpf: str
    password: str
    birthDate: date
    accountType: int = Field(ge=1, le=4)
    dailyWithdrawLimit: float = Field(gt=0, default=999)

    @field_validator('cpf')
    @classmethod
    def cpf_field_validator(cls, value: str) -> str:
        validators.validate_cpf(value)
        return value

    @field_validator('password')
    @classmethod
    def password_field_validator(cls, value: str) -> str:
        validators.validate_password(value)
        return value


class AccountOut(BaseModel):
    id: int
    flActive: bool
    person: PersonBasicOut


class AccountMeOut(BaseModel):
    id: int
    person: PersonOut
    balance: float
    flActive: bool
    accountType: int
    dailyWithdrawLimit: float
    todayWithdraw: float
