import datetime as dt
from sqlalchemy.orm import Session
from app.account.models import Account


def create_data(test_db: Session):
    account1 = Account(
        name='Tester1',
        cpf='58228952040',
        birthDate=dt.date(1980, 2, 15),
        password='Test#123',
        accountType=1,
    )

    account2 = Account(
        name='Tester2',
        cpf='38162813039',
        birthDate=dt.date(1980, 2, 15),
        password='Test#123',
        accountType=1,
    )

    test_db.add(account1)
    test_db.add(account2)

    test_db.commit()
