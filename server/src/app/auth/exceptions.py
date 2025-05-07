from fastapi import HTTPException, status


class InvalidCredentials(HTTPException):
    def __init__(self) -> None:
        """Will be raised if in the login attempt has invalid credentials."""
        self.detail = 'Credenciais Inválidas.'
        self.status_code = status.HTTP_403_FORBIDDEN


class CantLoginInBlockedAccount(HTTPException):
    def __init__(self) -> None:
        """Will be raised if in login attempt the account is blocked."""
        self.detail = 'Você não pode entrar em uma conta bloqueada, por favor entre em contato com o suporte para desbloquear sua conta.'
        self.status_code = status.HTTP_403_FORBIDDEN
