from fastapi import Depends
from dataclasses import dataclass
from core.db import get_db
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from app.account.schemas import AccountFilter
from app.account.models import Account, Person


@dataclass
class AccountRepository:
    db: Session = Depends(get_db)

    def get_all(
        self, filter: AccountFilter, account_id: int = None
    ) -> tuple[list[Account], int]:
        query = (
            select(Account, func.count(Account.id).over().label('total'))
            .join(Person, Account.person)
            .limit(filter.pageSize)
            .offset(
                filter.pageIndex - 1
                if filter.pageIndex == 1
                else (filter.pageIndex - 1) * filter.pageSize
            )
        )

        if account_id is not None:
            query = query.where(Account.id != account_id)

        if filter.search is not None:
            query = (
                query.join(Person, Person.id == Account.person_id)
                .where(Account.fl_active == True)
                .where(
                    or_(
                        Person.cpf.like(f'{filter.search}%'),
                        Person.name.like(f'%{filter.search}%'),
                    )
                )
            )

        results = self.db.execute(query).all()

        data = [result[0] for result in results]
        total = results[0]._asdict().get('total') if len(results) > 0 else 0

        return data, total

    def get_by_id(self, id: int) -> Account | None:
        query = select(Account).where(Account.id == id)
        return self.db.execute(query).scalars().first()

    def get_by_cpf(self, cpf: str, active: bool = None) -> Account | None:
        query = (
            select(Account)
            .join(Person, Account.person_id == Person.id)
            .where(Person.cpf == cpf)
        )

        if active is not None:
            query = query.where(Account.fl_active == active)

        return self.db.execute(query).scalars().first()

    def save(self, account: Account) -> Account:
        if account.id is None:
            self.db.add(account)

        self.db.commit()
        return account
