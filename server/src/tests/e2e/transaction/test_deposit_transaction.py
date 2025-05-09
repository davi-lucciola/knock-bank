import pytest
from fastapi import status
from fastapi.testclient import TestClient
from tests.mocks.transaction import money_in
from app.transaction.schemas import TransactionFilter
from app.transaction.enums import TransactionType
from app.transaction.repository import TransactionRepository
from app.account.repository import AccountRepository


# ------------ Deposit Transactions Tests --------------
@pytest.mark.transaction
def test_deposit_unauthorized(client: TestClient):
    # Test
    data = money_in()
    response = client.post('/api/transaction/deposit', json=data)

    # Assertion
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') is not None
    assert json.get('message') == 'É obrigatório estar autenticado.'


@pytest.mark.transaction
def test_deposit_required_fields(client: TestClient, authorization: dict):
    # Test
    data = {}
    response = client.post('/api/transaction/deposit', json=data, headers=authorization)

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
def test_deposit_invalid_money(client: TestClient, authorization: dict):
    # Test
    data = money_in()
    data['money'] = -200
    response = client.post('/api/transaction/deposit', json=data, headers=authorization)

    # Assertion
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('money')[0] == 'O valor da transação deve ser maior que zero.'


@pytest.mark.transaction
def test_deposit_successfully(
    client: TestClient,
    authorization: dict,
    account_repository: AccountRepository,
    transaction_repository: TransactionRepository,
):
    # Setup
    data = money_in()

    account_id = 1
    account = account_repository.get_by_id(account_id)

    account.balance = 0
    account = account_repository.save(account)

    assert account.balance == 0

    # Execution
    response = client.post('/api/transaction/deposit', json=data, headers=authorization)

    # Assertion
    assert response.status_code == status.HTTP_200_OK
    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Deposito realizado com sucesso.'

    account_repository.db.expire(account)
    assert float(account.balance) == data['money']

    filter = TransactionFilter()
    transactions, total = transaction_repository.get_all(filter, account_id)

    assert transactions is not None
    assert total != 0
    assert transactions[0].account_id == account_id
    assert abs(float(transactions[0].money)) == data['money']
    assert transactions[0].transaction_type == TransactionType.DEPOSIT.value[0]
    assert transactions[0].origin_account_id is None
