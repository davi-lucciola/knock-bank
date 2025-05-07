from fastapi import HTTPException, status


class TransactionNotFound(HTTPException):
    def __init__(self) -> None:
        '''Raised when transaction is not found by path parameter.'''
        self.detail = 'Transação não Encontrada'
        self.status_code = status.HTTP_404_NOT_FOUND


class InsuficientBalance(HTTPException):
    def __init__(self) -> None:
        '''Raised when a withdraw is being executed, but the user does not have balance'''
        self.detail = 'Saldo insuficiente.'
        self.status_code = status.HTTP_400_BAD_REQUEST


class DailyWithdrawLimitExceeded(HTTPException):
    def __init__(self) -> None:
        '''Raised when the user exceededs the daily withdraw limit.'''
        self.detail = 'Limite de saque diário excedido.'
        self.status_code = status.HTTP_400_BAD_REQUEST


class CantTransferForYourself(HTTPException):
    def __init__(self) -> None:
        '''Raised when the user try to transfer for yourself (can happen just via API)'''
        self.detail = 'Não é possivel realizar uma trânsferencia para sua propria conta, por favor realize um deposito.'
        self.status_code = status.HTTP_400_BAD_REQUEST


class ReciverAccountNotFound(HTTPException):
    def __init__(self) -> None:
        '''Raised when the reciver account is not found.'''
        self.detail = 'Conta destino não encontrada.'
        self.status_code = status.HTTP_404_NOT_FOUND
