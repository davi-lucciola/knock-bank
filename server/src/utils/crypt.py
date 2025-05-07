from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(plain_text: str) -> str:
    return pwd_context.hash(plain_text)


def check_hash(plain_text: str, hash: str) -> bool:
    return pwd_context.verify(plain_text, hash)
