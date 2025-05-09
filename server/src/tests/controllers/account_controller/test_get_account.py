from fastapi import status
from fastapi.testclient import TestClient
from tests.conftest import AuthorizationHeader


# ------------ Get My Account Test ---------------
def test_get_my_account_unauthorized(client: TestClient):
    response = client.get('/api/account/me')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    json: dict = response.json()
    assert json is not None

    # assert json.get('message') is not None
    # assert json.get('message') == 'É obrigatório estar autenticado.'


def test_get_my_account_successfully(
    client: TestClient, authorization: AuthorizationHeader
):
    response = client.get('/api/account/me', headers=authorization)

    assert response.status_code == status.HTTP_200_OK

    json: dict = response.json()
    assert json is not None

    assert json.get('id') is not None
    assert json.get('accountType') is not None
    assert json.get('flActive') is not None
    assert json.get('dailyWithdrawLimit') is not None
    assert json.get('person') is not None
    assert json.get('person').get('id') is not None
    assert json.get('person').get('name') is not None
    assert json.get('person').get('cpf') is not None
    assert json.get('person').get('birthDate') is not None


# ------------ Get Other Accounts Test ---------------
def test_get_other_accounts_unauthorized(client: TestClient):
    response = client.get('/api/account')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') is not None
    assert json.get('message') == 'É obrigatório estar autenticado.'


def test_get_other_accounts(client: TestClient, authorization: dict):
    response = client.get('/api/account', headers=authorization)

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

    assert data[0].get('id') is not None
    assert data[0].get('accountType') is None
    assert data[0].get('flActive') is not None
    assert data[0].get('dailyWithdrawLimit') is None
    assert data[0].get('person') is not None
    assert data[0].get('person').get('id') is not None
    assert data[0].get('person').get('name') is not None
    assert data[0].get('person').get('cpf') is not None
    assert data[0].get('person').get('cpf') == '***.628.130-**'
    assert data[0].get('person').get('birthDate') is None


def test_get_other_accounts_search_find_content_by_name(client: TestClient, authorization: dict):
    query = {'search': 'Tester2'}
    response = client.get('/api/account', params=query, headers=authorization)

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
    assert len(data) == 1

    assert data[0].get('id') is not None
    assert data[0].get('accountType') is None
    assert data[0].get('flActive') is not None
    assert data[0].get('dailyWithdrawLimit') is None
    assert data[0].get('person') is not None
    assert data[0].get('person').get('id') is not None
    assert data[0].get('person').get('name') is not None
    assert data[0].get('person').get('name') == query.get('search')
    assert data[0].get('person').get('cpf') is not None
    assert data[0].get('person').get('cpf') == '***.628.130-**'
    assert data[0].get('person').get('birthDate') is None


def test_get_other_accounts_search_no_content(client: TestClient, authorization: dict):
    query = {'search': 'NOT EXISTS PERSON'}
    response = client.get('/api/account', params=query, headers=authorization)

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
    assert len(data) == 0
