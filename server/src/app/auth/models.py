import typing as t
from utils import crypt
from core.db import BaseModel, Long
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship


if t.TYPE_CHECKING:
    from app.account.models import Account


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Long, primary_key=True, autoincrement=True)
    password: Mapped[str] = Column(String(255), nullable=False)
    token: Mapped[str] = Column(String(255), nullable=True)
    refresh_token: Mapped[str] = Column(String(255), nullable=True)

    account: Mapped['Account'] = relationship(
        'Account', lazy='joined', back_populates='user'
    )

    def __init__(self, password: str) -> None:
        self.password = crypt.hash(password)

    def verify_password_hash(self, password: str) -> bool:
        return crypt.check_hash(password, self.password)
