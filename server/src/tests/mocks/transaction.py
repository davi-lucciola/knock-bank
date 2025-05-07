from app.transaction.schemas import MoneyIn, TransactionIn, TransactionFilter


def money_in():
    return MoneyIn(money=800).model_dump(mode='json')


def transaction_in():
    # accountId from "Tester2"
    return TransactionIn(money=800, accountId=2).model_dump(mode='json')


def transaction_filter():
    return TransactionFilter(pageIndex=1, pageSize=10).model_dump(mode='json')
