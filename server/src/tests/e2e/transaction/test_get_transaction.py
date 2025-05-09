import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.transaction.models import Transaction
from app.transaction.enums import TransactionType
from app.transaction.repository import TransactionRepository
from app.account.repository import AccountRepository


# ------------ Get Transactions Tests --------------
@pytest.mark.transaction
def test_get_my_transactions_unauthorized(client: TestClient):
    # Test
    response = client.get('/api/transaction')

    # Assertion
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') is not None
    assert json.get('message') == 'É obrigatório estar autenticado.'


@pytest.mark.transaction
def test_get_my_transactions(
    client: TestClient,
    authorization: dict,
    account_repository: AccountRepository,
    transaction_repository: TransactionRepository,
):
    # Setup
    account_id = 1
    origin_account_id = 2

    account = account_repository.get_by_id(account_id)
    account_reciver = account_repository.get_by_id(origin_account_id)

    transaction1 = Transaction(
        money=-200, transaction_type=TransactionType.WITHDRAW, account=account
    )
    transaction_repository.save(transaction1)

    transaction2 = Transaction(
        money=156.04,
        transaction_type=TransactionType.DEPOSIT,
        account=account,
        origin_account=account_reciver,
    )
    transaction_repository.save(transaction2)

    # Test
    response = client.get('/api/transaction', headers=authorization)

    # Assertion
    assert response.status_code == status.HTTP_200_OK

    json: dict = response.json()
    assert json is not None

    assert json.get('pageIndex') is not None
    assert json.get('pageSize') is not None
    assert json.get('total') is not None
    assert json.get('totalPages') is not None

    data: list[dict] = json.get('data')
    assert data is not None
    assert isinstance(data, list)
    assert len(data) != 0

    # Last transctions saved must be the first
    assert data[0].get('id') is not None
    assert data[0].get('money') is not None
    assert data[0].get('money') == 156.04
    assert data[0].get('dateTime') is not None
    assert data[0].get('transactionType') is not None
    assert data[0].get('transactionType') == TransactionType.DEPOSIT.value[0]
    assert data[0].get('account') is not None
    assert data[0].get('account').get('id') == account_id
    assert data[0].get('originAccount') is not None
    assert data[0].get('originAccount').get('id') == origin_account_id

    assert data[1].get('id') is not None
    assert data[1].get('money') is not None
    assert data[1].get('money') == -200
    assert data[1].get('dateTime') is not None
    assert data[1].get('transactionType') is not None
    assert data[1].get('transactionType') == TransactionType.WITHDRAW.value[0]
    assert data[1].get('account') is not None
    assert data[1].get('account').get('id') == account_id
    assert data[1].get('originAccount') is None
