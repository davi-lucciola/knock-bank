import pytest
from fastapi import status
from fastapi.testclient import TestClient
from tests.mocks.transaction import transaction_in
from app.transaction.schemas import TransactionFilter
from app.transaction.enums import TransactionType
from app.transaction.repository import TransactionRepository
from app.account.repository import AccountRepository


# ------------ Withdraw Transactions Tests --------------
@pytest.mark.transaction
def test_withdraw_unauthorized(client: TestClient):
    # Test
    data = transaction_in()
    response = client.post('/api/transaction/withdraw', json=data)

    # Assertion
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') is not None
    assert json.get('message') == 'É obrigatório estar autenticado.'


@pytest.mark.transaction
def test_withdraw_required_fields(client: TestClient, authorization: dict):
    # Test
    data = {}
    response = client.post(
        '/api/transaction/withdraw', json=data, headers=authorization
    )

    # Assertion
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('money')[0] == 'Missing data for required field.'


@pytest.mark.transaction
def test_withdraw_invalid_money(client: TestClient, authorization: dict):
    # Test
    data = transaction_in()
    data['money'] = -200
    response = client.post(
        '/api/transaction/withdraw', json=data, headers=authorization
    )

    # Assertion
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}


@pytest.mark.transaction
def test_withdraw_no_available_balance(
    client: TestClient, authorization: dict, account_repository: AccountRepository
):
    data = transaction_in()
    account_id = 1
    account = account_repository.get_by_id(account_id)

    assert account.balance < data['money']

    response = client.post(
        '/api/transaction/withdraw', json=data, headers=authorization
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Saldo insuficiente.'


@pytest.mark.transaction
def test_withdraw_no_daily_limit_available(
    client: TestClient,
    authorization: dict,
    account_repository: AccountRepository,
):
    data = transaction_in()
    data['money'] = 2000
    account_id = 1
    account = account_repository.get_by_id(account_id)

    account.balance = 3000
    account = account_repository.save(account)

    assert account.balance > data['money']
    assert account.daily_withdraw_limit < data['money']

    response = client.post(
        '/api/transaction/withdraw', json=data, headers=authorization
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Limite de saque diário excedido.'


@pytest.mark.transaction
def test_withdraw_successfully(
    client: TestClient,
    authorization: dict,
    account_repository: AccountRepository,
    transaction_repository: TransactionRepository,
):
    data = transaction_in()
    initial_balance = 800

    account_id = 1
    account = account_repository.get_by_id(account_id)

    account.balance = initial_balance
    account = account_repository.save(account)

    assert account.balance >= data['money']
    assert account.daily_withdraw_limit > data['money']

    response = client.post(
        '/api/transaction/withdraw', json=data, headers=authorization
    )

    assert response.status_code == status.HTTP_200_OK

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Saque realizado com sucesso.'

    account_repository.db.expire(account)
    assert float(account.balance) == initial_balance - data['money']
    assert (
        abs(float(transaction_repository.get_total_today_withdraw(account_id)))
        == data['money']
    )

    filter = TransactionFilter()
    transactions, total = transaction_repository.get_all(filter, account_id)
    assert transactions is not None
    assert total != 0
    assert transactions[0].account_id == account_id
    assert abs(float(transactions[0].money)) == data['money']
    assert transactions[0].transaction_type == TransactionType.WITHDRAW.value[0]
    assert transactions[0].origin_account_id is None
