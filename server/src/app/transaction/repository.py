from fastapi import Depends
from datetime import date
from decimal import Decimal
from dataclasses import dataclass
from sqlalchemy import text, select, func
from sqlalchemy.orm import Session
from core.db import get_db
from app.transaction.models import Transaction
from app.transaction.enums import TransactionType
from app.transaction.schemas import TransactionMonthResumeNumericOut, TransactionFilter
from app.transaction.resumes import create_year_transaction_resume_by_month


@dataclass
class TransactionRepository:
    db: Session = Depends(get_db)

    def get_all(
        self,
        filter: TransactionFilter,
        account_id: int,
    ) -> tuple[list[Transaction], int]:
        query = (
            select(Transaction, func.count(Transaction.id).over().label('total'))
            .where(Transaction.account_id == account_id)
            .limit(filter.pageSize)
            .offset(
                filter.pageIndex - 1
                if filter.pageIndex == 1
                else (filter.pageIndex - 1) * filter.pageSize
            )
            .order_by(Transaction.date_time.desc())
        )

        if filter.transactionType is not None:
            query = query.where(Transaction.transaction_type == filter.transactionType)

        if filter.transactionDate is not None:
            query = query.where(
                func.date(Transaction.date_time) == filter.transactionDate
            )

        results = self.db.execute(query).all()

        data = [result[0] for result in results]
        total = results[0]._asdict().get('total') if len(results) > 0 else 0

        return data, total

    def get_total_today_withdraw(self, account_id: int) -> Decimal:
        query = (
            select(func.sum(Transaction.money))
            .where(Transaction.account_id == account_id)
            .where(func.date(Transaction.date_time) == (date.today()))
            .where(Transaction.transaction_type == TransactionType.WITHDRAW.value[0])
        )

        total = self.db.execute(query).scalars().first()
        return total if total is not None else Decimal(0)

    def get_this_year_transactions(self, account_id: int):
        query = text(
            """
            SELECT
                MONTH(t.date_time) as month,
                (CASE WHEN t.transaction_type = 1 
                    THEN 'Entrada'
                    ELSE 'Saída' 
                END) as label,
                SUM(ABS(t.money)) as amount
            FROM 
                transactions t
            WHERE 
                t.account_id = :account_id
                AND YEAR(t.date_time) = YEAR(CURRENT_TIMESTAMP())
            GROUP BY 
                label, month
            ORDER BY 
                month, label
            """
        )

        data = self.db.execute(query, {'account_id': account_id}).all()
        data = [TransactionMonthResumeNumericOut(**row._asdict()) for row in data]
        return create_year_transaction_resume_by_month(data)

    def get_by_id(self, id: int) -> Transaction | None:
        query = select(Transaction).where(Transaction.id == id)
        return self.db.execute(query).scalars().first()

    def save(self, transaction: Transaction) -> Transaction:
        if transaction.id is None:
            self.db.add(transaction)

        self.db.commit()
        return transaction

    def save_all(self, transactions: list[Transaction]) -> None:
        self.db.add_all(transactions)
        self.db.commit()
