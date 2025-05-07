from fastapi import HTTPException, status


class AccountNotFound(HTTPException):
    def __init__(self) -> None:
        """Raised when account is not found by path parameter."""
        self.detail = 'Conta não encontrada.'
        self.status_code = status.HTTP_404_NOT_FOUND


class AccountAlreadyExistsWithThisCPF(HTTPException):
    def __init__(self) -> None:
        """Raised when a account already exists with a cpf."""
        self.detail = 'Esse CPF já tem uma conta cadastrada.'
        self.status_code = status.HTTP_400_BAD_REQUEST


class AccountOwnerIsMinor(HTTPException):
    def __init__(self) -> None:
        """Raised when the account owner is minor."""
        self.detail = 'Você precisa ser maior de idade para criar uma conta.'
        self.status_code = status.HTTP_400_BAD_REQUEST


class CantUpdateAccount(HTTPException):
    def __init__(self) -> None:
        """Raised when the current user is trying to update other user account."""
        self.detail = 'Você não tem permissão para editar essa conta.'
        self.status_code = status.HTTP_403_FORBIDDEN


class CantUpdateDailyWithdrawLimit(HTTPException):
    def __init__(self) -> None:
        """Raised when a account owner tries to update the daily withdraw limit to less then he already withdraw today"""
        self.detail = 'Você não pode alterar o limite de saque diário para um menor do que já foi sacado hoje.'
        self.status_code = status.HTTP_400_BAD_REQUEST


class CantBlockAccount(HTTPException):
    def __init__(self) -> None:
        """Raised when the current user is trying to block other user account."""
        self.detail = 'Você não tem permissão para bloquear essa conta.'
        self.status_code = status.HTTP_403_FORBIDDEN
