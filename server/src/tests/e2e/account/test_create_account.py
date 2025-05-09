import pytest
import datetime as dt
from fastapi import status
from fastapi.testclient import TestClient
from app.account.repository import AccountRepository
from tests.mocks.account import create_account_in


# ------------ Create Account Tests --------------
# Schema Validation Tests
@pytest.mark.account
def test_create_account_missing_values(client: TestClient):
    data = {}
    response = client.post('/api/account', json=data)

    json: dict = response.json()
    assert json is not None
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('cpf')[0] == 'Missing data for required field.'
    # assert errors.get('accountType')[0] == 'Missing data for required field.'
    # assert errors.get('birthDate')[0] == 'Missing data for required field.'
    # assert errors.get('password')[0] == 'Missing data for required field.'


@pytest.mark.account
def test_create_account_invalid_cpf(client: TestClient):
    data = create_account_in()
    data['cpf'] = '58901211078'

    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('cpf')[0] == 'Cpf inválido.'


@pytest.mark.account
def test_create_account_invalid_password_lenght(client: TestClient):
    data = create_account_in()
    data['password'] = 'tes'
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('password')[0] == 'A senha deve conter no minímo 8 caracteres.'


@pytest.mark.account
def test_create_account_password_with_no_lowercase(client: TestClient):
    data = create_account_in()
    data['password'] = 'TESTE#123'
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('password')[0] == 'A senha deve conter letras minúsculas.'


@pytest.mark.account
def test_create_account_password_with_no_uppercase(client: TestClient):
    data = create_account_in()
    data['password'] = 'teste#123'
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('password')[0] == 'A senha deve conter letras maiúsculas.'


@pytest.mark.account
def test_create_account_password_with_no_numbers(client: TestClient):
    data = create_account_in()
    data['password'] = 'teste#ASD'
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('password')[0] == 'A senha deve conter numeros.'


@pytest.mark.account
def test_create_account_password_with_special_characters(client: TestClient):
    data = create_account_in()
    data['password'] = 'Teste1234'
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Validation error'
    assert json.get('detail') is not None
    assert json.get('detail') != {}

    # errors: dict = json.get('detail').get('json')
    # assert errors.get('password')[0] == 'A senha deve conter caracteres especiais.'


# Bussiness Rules
@pytest.mark.account
def test_create_account_minor_not_allowed(client: TestClient):
    data = create_account_in()
    minor_age = dt.date.today() - dt.timedelta(days=365 * 6)  # 6 Years
    data['birthDate'] = minor_age.isoformat()
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    json: dict = response.json()
    assert json is not None

    assert (
        json.get('message') == 'Você precisa ser maior de idade para criar uma conta.'
    )


@pytest.mark.account
def test_create_account_cpf_already_exists(client: TestClient):
    data = create_account_in()
    data['cpf'] = '58228952040'  # Tester1 CPF
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Esse CPF já tem uma conta cadastrada.'


@pytest.mark.account
def test_create_account_successfully(
    client: TestClient, account_repository: AccountRepository
):
    data = create_account_in()
    response = client.post('/api/account', json=data)

    assert response.status_code == status.HTTP_201_CREATED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Conta cadastrada com sucesso.'

    account = account_repository.get_by_cpf(data['cpf'])

    assert account is not None
    assert account.person.name == data['name']
    assert account.person.cpf == data['cpf']
    assert account.user.verify_password_hash(data['password']) is True
