from fastapi import APIRouter, Query, Depends
from core.security import get_current_user
from app.auth.models import User
from app.transaction.schemas import *
from app.transaction.service import TransactionService
from utils.schemas import PaginationResponse


transaction_router = APIRouter(tags=['Transaction'], prefix='/api/transaction')


@transaction_router.get('/')
def get_all_transactions(
    filter: TransactionFilter = Query(TransactionFilter),
    user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(TransactionService),
) -> PaginationResponse[TransactionOut]:
    """
    Endpoint para buscar transações realizadas pelo usuário.\n
    Trás as transações de forma paginada.
    """
    return transaction_service.get_all(filter, user.account.id)


@transaction_router.get('/resume')
def get_month_transactions_resume(
    user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(TransactionService),
) -> list[TransactionMonthResumeOut]:
    """Endpoint para buscar resumo de transações realizadas no ano."""
    return transaction_service.get_month_transactions_resume(user.account.id)


@transaction_router.get('/{id}', dependencies=[Depends(get_current_user)])
def detail_transaction(
    id: int, transaction_service: TransactionService = Depends(TransactionService)
) -> TransactionOut:
    """Endpoint para detalhar uma determinada transação."""
    transaction = transaction_service.get_by_id(id)
    return transaction.to_json()


@transaction_router.post('/withdraw')
def withdraw_money(
    money_in: MoneyIn,
    user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(TransactionService),
):
    """Endpoint para realizar um saque da conta logada."""
    transaction_in = TransactionIn(money=money_in.money, accountId=user.account.id)

    transaction_service.withdraw(transaction_in)
    return {'message': 'Saque realizado com sucesso.'}


@transaction_router.post('/deposit')
def deposit_money(
    money_in: MoneyIn,
    user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(TransactionService),
):
    """Endpoint para realizar um depósito na conta logada."""
    transaction_in = TransactionIn(money=money_in.money, accountId=user.account.id)

    transaction_service.deposit(transaction_in)
    return {'message': 'Deposito realizado com sucesso.'}


@transaction_router.post('/transfer')
def transfer_money(
    transaction_in: TransactionIn,
    user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(TransactionService),
):
    """Endpoint para realizar uma transferencia para outra conta registrada."""
    transaction_transfer_in = TransactionTransferIn(
        money=transaction_in.money,
        accountId=transaction_in.accountId,
        senderAccountId=user.account.id,
    )

    transaction_service.transfer(transaction_transfer_in)
    return {'message': 'Transferência realizada com sucesso.'}
