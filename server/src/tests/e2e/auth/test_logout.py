import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.account.repository import AccountRepository


# ------------ Logout User Tests --------------
@pytest.mark.auth
def test_logout_unauthorized(client: TestClient):
    response = client.delete('/api/logout')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    json: dict = response.json()
    assert json is not None

    assert json.get('message') is not None
    assert json.get('message') == 'É obrigatório estar autenticado.'


@pytest.mark.auth
def test_logout_successfully(
    client: TestClient, authorization: dict, account_repository: AccountRepository
):
    response = client.delete('/api/logout', headers=authorization)

    assert response.status_code == status.HTTP_200_OK

    json: dict = response.json()
    assert json is not None

    assert json.get('message') is not None
    assert json.get('message') == 'Conta desconectada com sucesso.'

    account_id = 1
    account = account_repository.get_by_id(account_id)
    assert account.user.token is None
    assert account.user.refresh_token is None
