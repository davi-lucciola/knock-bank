from decimal import Decimal
from datetime import date
from app.auth.models import User
from app.account.schemas import UpdateAccountIn
from core.db import BaseModel, Long
from sqlalchemy import Column, ForeignKey, String, Date, Integer, Numeric, Boolean
from sqlalchemy.orm import Mapped, relationship


class Person(BaseModel):
    __tablename__ = 'persons'

    id: Mapped[int] = Column(Long, primary_key=True, autoincrement=True)
    cpf: Mapped[str] = Column(String(11), nullable=False, unique=True)
    name: Mapped[str] = Column(String(255), nullable=False)
    birth_date: Mapped[date] = Column(Date, nullable=False)

    account: Mapped['Account'] = relationship('Account', back_populates='person')

    def __str__(self) -> str:
        return f'<Person - {self.name}>'

    def __init__(self, name: str, cpf: str, birth_date: date) -> None:
        self.name = name
        self.cpf = cpf
        self.birth_date = birth_date


class Account(BaseModel):
    __tablename__ = 'accounts'

    id: Mapped[int] = Column(Long, primary_key=True, autoincrement=True)
    balance: Mapped[Decimal] = Column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal(0),
    )
    fl_active: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    account_type: Mapped[int] = Column(Integer, nullable=False)
    daily_withdraw_limit: Mapped[Decimal] = Column(
        Numeric(10, 2), nullable=False, default=Decimal(999)
    )

    person_id: Mapped[int] = Column(
        Long, ForeignKey('persons.id'), nullable=False, unique=True
    )
    person: Mapped['Person'] = relationship('Person', back_populates='account')

    user_id: Mapped[int] = Column(
        Long, ForeignKey('users.id'), nullable=False, unique=True
    )
    user: Mapped['User'] = relationship(
        'User', cascade='save-update', back_populates='account'
    )

    def __init__(
        self,
        name: str,
        cpf: str,
        birthDate: date,
        password: str,
        accountType: int,
        dailyWithdrawLimit: float = 999,
    ) -> None:
        self.person = Person(name, cpf, birthDate)
        self.user = User(password)
        self.account_type = accountType
        self.balance = 0
        self.daily_withdraw_limit = dailyWithdrawLimit
        self.fl_active = True

    def __str__(self) -> str:
        return f'<Account - {self.person.name} | {self.id}>'

    def update(self, data: UpdateAccountIn) -> None:
        self.person.name = data.name
        self.person.birth_date = data.birthDate
        self.account_type = data.accountType
        self.daily_withdraw_limit = data.dailyWithdrawLimit

    def to_json(self, mask_cpf: bool = False) -> dict:
        return {
            'id': self.id,
            'balance': self.balance,
            'flActive': self.fl_active,
            'person': {
                'id': self.person.id,
                'name': self.person.name,
                'cpf': (
                    self.person.cpf
                    if mask_cpf is False
                    else '***.'
                    + self.person.cpf[3:6]
                    + '.'
                    + self.person.cpf[6:9]
                    + '-**'
                ),
                'birthDate': self.person.birth_date,
            },
            'accountType': self.account_type,
            'dailyWithdrawLimit': float(self.daily_withdraw_limit),
        }
