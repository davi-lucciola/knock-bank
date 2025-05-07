import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from typing import AsyncGenerator, Generator, TypedDict
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.pool import StaticPool

import tests.mocks as mocks

from app import create_app
from core.db import BaseModel, get_db

from app.auth.schemas import TokenIn
from app.auth.repository import UserRepository
from app.account.repository import AccountRepository
from app.transaction.repository import TransactionRepository


# Database Test Config
DATABASE_URL = 'sqlite:///:memory:'


test_engine: Engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool
)

TestSessionLocal: Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
    bind=test_engine,
)


async def override_test_db() -> AsyncGenerator[Session, None]:
    session: Session = TestSessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope='module')
def test_db() -> Generator[Session, None, None]:
    session: Session = TestSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope='module')
def user_repository(test_db: Session):
    return UserRepository(test_db)


@pytest.fixture(scope='module')
def account_repository(test_db: Session):
    return AccountRepository(test_db)


@pytest.fixture(scope='module')
def transaction_repository(test_db: Session):
    return TransactionRepository(test_db)


# App Test Config
@pytest.fixture(scope='module')
def test_app(test_db: Session):
    BaseModel.metadata.create_all(bind=test_engine)

    mocks.create_data(test_db)

    test_app = create_app()
    test_app.dependency_overrides[get_db] = override_test_db

    yield test_app

    BaseModel.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope='module')
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


# Authorization Test Config
class AuthorizationHeader(TypedDict):
    Authorization: str


@pytest.fixture(scope='function')
def authorization(client: TestClient):
    payload = TokenIn(cpf='58228952040', password='Test#123')
    response = client.post('/api/login', json=payload.model_dump(mode='json'))

    assert response.status_code == status.HTTP_200_OK

    data: dict = response.json()
    assert data is not None

    access_token = data.get('accessToken')
    assert access_token is not None

    headers = AuthorizationHeader(Authorization=f'Bearer {access_token}')
    return headers
