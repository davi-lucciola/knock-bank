from fastapi import status
from fastapi.testclient import TestClient
from core import security
from app.auth.schemas import TokenIn
from app.account.repository import AccountRepository


# ------------ Login User Tests --------------
def test_login_invalid_credentials_wrong_password(client: TestClient):
    payload = TokenIn(cpf='58228952040', password='Test#12')
    response = client.post('/api/login', json=payload.model_dump(mode='json'))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Credenciais Inválidas.'


def test_login_invalid_blocked_account(
    client: TestClient, account_repository: AccountRepository
):
    payload = TokenIn(cpf='58228952040', password='Test#123')

    account = account_repository.get_by_cpf(payload.cpf)
    account.fl_active = False
    account_repository.save(account)

    response = client.post('/api/login', json=payload.model_dump(mode='json'))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    json: dict = response.json()
    assert json is not None

    assert (
        json.get('message')
        == 'Você não pode entrar em uma conta bloqueada, por favor entre em contato com o suporte para desbloquear sua conta.'
    )


def test_login_invalid_inexistent_user(client: TestClient):
    payload = TokenIn(cpf='58228958676', password='qualquer')
    response = client.post('/api/login', json=payload.model_dump(mode='json'))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    json: dict = response.json()
    assert json is not None

    assert json.get('message') == 'Credenciais Inválidas.'


def test_login_successfully(client: TestClient, account_repository: AccountRepository):
    payload = TokenIn(cpf='38162813039', password='Test#123')
    response = client.post('/api/login', json=payload.model_dump(mode='json'))

    assert response.status_code == status.HTTP_200_OK

    json: dict = response.json()
    assert json is not None

    assert json.get('type') == 'bearer'

    token = json.get('accessToken')
    assert token is not None

    token_payload = security.decode_token(token)

    assert int(token_payload.get('sub')) == 2
    account = account_repository.get_by_cpf(payload.cpf)
    assert account.user.token == token
