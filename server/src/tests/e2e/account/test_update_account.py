import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import AuthorizationHeader
from tests.mocks.account import update_account_in
from app.account.repository import AccountRepository
from app.transaction.models import Transaction
from app.transaction.enums import TransactionType
from app.transaction.repository import TransactionRepository


# ------------ Update Account Tests --------------
@pytest.mark.account
def test_update_account_unauthorized(client: TestClient):
    account_id = 1
    data = {}
    # Account with id 1 is "Tester1"
    response = client.put(f'/api/account/{account_id}', json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') is not None
    assert json.get('message') == 'É obrigatório estar autenticado.'


# Schema Validation Tests
@pytest.mark.account
def test_update_account_missing_values(client: TestClient, authorization: dict):
    account_id = 1
    data = {}
    # Account with id 1 is "Tester1"
    response = client.put(
        f'/api/account/{account_id}', json=data, headers=authorization
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('name')[0] == 'Missing data for required field.'
    # assert errors.get('accountType')[0] == 'Missing data for required field.'
    # assert errors.get('birthDate')[0] == 'Missing data for required field.'


@pytest.mark.account
def test_update_invalid_account_type_and_withdraw_limit(
    client: TestClient, authorization: dict
):
    account_id = 1
    data = update_account_in()
    data['accountType'] = 0
    data['dailyWithdrawLimit'] = -1

    response = client.put(
        f'/api/account/{account_id}', json=data, headers=authorization
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert (
    #     errors.get('accountType')[0] == 'Tipo de Conta Inválida. Deve ser 1, 2, 3 ou 4.'
    # )
    # assert (
    #     errors.get('dailyWithdrawLimit')[0]
    #     == 'O limite de saque diário deve maior que zero.'
    # )


# Bussiness Rules
@pytest.mark.account
def test_update_account_not_found(client: TestClient, authorization: dict):
    account_id = 0
    data = update_account_in()
    response = client.put(
        f'/api/account/{account_id}', json=data, headers=authorization
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Conta não encontrada.'


@pytest.mark.account
def test_update_account_forbidden(client: TestClient, authorization: dict):
    account_id = 2
    data = update_account_in()
    # AccountId 2 is for "Tester2", but the token are from "Tester1"
    response = client.put(
        f'/api/account/{account_id}', json=data, headers=authorization
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Você não tem permissão para editar essa conta.'


@pytest.mark.account
def test_update_account_daily_withdraw_limit_not_possible(
    client: TestClient,
    authorization: AuthorizationHeader,
    account_repository: AccountRepository,
    transaction_repository: TransactionRepository,
):
    # Setup
    account_id = 1

    account = account_repository.get_by_id(account_id)
    account.balance = 900
    account_repository.save(account)

    transaction = Transaction(
        money=-800, transaction_type=TransactionType.WITHDRAW, account=account
    )
    transaction_repository.save(transaction)

    data = update_account_in()
    data['dailyWithdrawLimit'] = 600  # Smaller than what the account spend today

    # Test
    response = client.put(
        f'/api/account/{account_id}', json=data, headers=authorization
    )

    # Assertion
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    json: dict = response.json()
    assert json is not None

    assert (
        json.get('message')
        == 'Você não pode alterar o limite de saque diário para um menor do que já foi sacado hoje.'
    )


@pytest.mark.account
def test_update_account_successfully(
    client: TestClient, authorization: dict, account_repository: AccountRepository
):
    # Setup
    account_id = 1
    data = update_account_in()

    # Test
    response = client.put(
        f'/api/account/{account_id}', json=data, headers=authorization
    )

    # Assertion
    assert response.status_code == status.HTTP_202_ACCEPTED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Conta atualizada com sucesso.'

    account = account_repository.get_by_id(account_id)

    assert account.person.name == data['name']
    assert account.person.birth_date.strftime('%Y-%m-%d') == data['birthDate']
    assert account.account_type == data['accountType']
    assert float(account.daily_withdraw_limit) == data['dailyWithdrawLimit']
