import jwt
from core.config import settings
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.db import get_db
from app.auth.models import User


bearer_security = HTTPBearer()
bearer_security.auto_error = False


def encode_token(payload: dict) -> str:
    return jwt.encode(payload, settings.TOKEN_SECRET, settings.ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.TOKEN_SECRET, algorithms=[settings.ALGORITHM])


def create_token(user_id: int) -> str:
    initiated_at = datetime.now(timezone.utc)
    expires_on = initiated_at + timedelta(seconds=settings.EXPIRATION_SECONDS)

    token_payload = {'exp': expires_on, 'iat': initiated_at, 'sub': str(user_id)}

    access_token: str = encode_token(token_payload)
    return access_token


def get_current_user(
    db: Session = Depends(get_db),
    auth: HTTPAuthorizationCredentials | None = Security(bearer_security),
) -> User:
    if auth is None:
        raise HTTPException(
            detail='É obrigatório estar autenticado.',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        payload = decode_token(auth.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            detail='Token Expirado.', status_code=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.PyJWTError:
        raise HTTPException(
            detail='Token inválido.', status_code=status.HTTP_401_UNAUTHORIZED
        )

    user_id = int(payload.get('sub'))
    query = select(User).where(User.id == user_id)
    user = db.execute(query).scalars().first()

    if user is None:
        raise HTTPException(
            detail='Usuário não encontrado.',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return user
