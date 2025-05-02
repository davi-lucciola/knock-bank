import logging
from datetime import date
from decimal import Decimal
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, select, func
from knockbankapi.domain.errors import InfraError
from knockbankapi.domain.dto import (
    PaginationResponseDTO,
    TransactionQueryDTO,
    PaginationBuilder,
    TransactionResumeBuilder,
)
from knockbankapi.domain.models import Transaction, TransactionType


@dataclass
class TransactionRepository:
    db: SQLAlchemy

    def get_all(
        self,
        filter: TransactionQueryDTO,
        account_id: int,
    ) -> PaginationResponseDTO[Transaction]:
        query = (
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .order_by(Transaction.id.desc())
        )

        if filter.get('transactionType') is not None:
            query = query.where(
                Transaction.transaction_type == filter.get('transactionType')
            )

        if filter.get('transactionDate') is not None:
            query = query.where(
                func.date(Transaction.date_time) == filter.get('transactionDate')
            )

        data = self.db.paginate(
            query, page=filter['pageIndex'], per_page=filter['pageSize']
        )

        return PaginationBuilder.build(
            data.items, data.total, data.pages, filter['pageIndex'], filter['pageSize']
        )

    def get_total_today_withdraw(self, account_id: int) -> Decimal:
        total = (
            self.db.session.query(func.sum(Transaction.money))
            .where(Transaction.account_id == account_id)
            .where(func.date(Transaction.date_time) == (date.today()))
            .where(Transaction.transaction_type == TransactionType.WITHDRAW.value[0])
            .first()[0]
        )

        return total if total is not None else Decimal(0)

    def get_this_year_transactions(self, account_id: int):
        query = text(
            '''
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
        '''
        )

        data = self.db.session.execute(query, {'account_id': account_id}).all()
        return TransactionResumeBuilder.build(
            [{'month': row[0], 'label': row[1], 'amount': row[2]} for row in data]
        )

    def get_by_id(self, id: int) -> Transaction | None:
        return self.db.session.query(Transaction).get(id)

    def save(self, transaction: Transaction) -> Transaction:
        try:
            if transaction.id is None:
                self.db.session.add(transaction)
            self.db.session.commit()
            return transaction
        except Exception as err:
            logging.error(err)
            self.db.session.rollback()
            raise InfraError('Houve um error ao salvar a transação.')

    def save_all(self, transactions: list[Transaction]):
        try:
            self.db.session.add_all(transactions)
            self.db.session.commit()
        except Exception as err:
            logging.error(err)
            self.db.session.rollback()
            raise InfraError('Houve um error ao salvar as transações.')
