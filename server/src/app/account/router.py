from fastapi import APIRouter, Depends, Query, status
from core.security import get_current_user
from app.auth.models import User
from app.account.schemas import *
from app.account.models import Account
from app.account.service import AccountService
from app.transaction.repository import TransactionRepository
from utils.schemas import PaginationResponse


account_router = APIRouter(tags=['Account'], prefix='/api/account')


@account_router.get('/me')
def get_auth_account(
    user: User = Depends(get_current_user),
    transaction_repository: TransactionRepository = Depends(TransactionRepository),
) -> AccountMeOut:
    """Endpoint para buscar os dados da conta logada."""
    account: Account = user.account
    today_withdraw = transaction_repository.get_total_today_withdraw(account.id)

    account_json = account.to_json()
    account_json.update({'todayWithdraw': float(-(today_withdraw))})

    return AccountMeOut(**account_json)


@account_router.get('/')
def get_all(
    filter: AccountFilter = Query(AccountFilter),
    user: User = Depends(get_current_user),
    account_service: AccountService = Depends(AccountService),
) -> PaginationResponse[AccountOut]:
    """
    Endpoint para buscar contas cadastradas.\n
    Não trás a propria conta que está consultando.
    """
    return account_service.get_all(filter, user.account.id)


@account_router.post('/', status_code=status.HTTP_201_CREATED)
def create_account(
    account_in: AccountIn, account_service: AccountService = Depends(AccountService)
):
    """Endpoint para cadastrar uma nova conta."""
    account = account_service.create(account_in)

    return {
        'message': 'Conta cadastrada com sucesso.',
        'detail': {'created_id': account.id},
    }


@account_router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_account(
    id: int,
    update_account_in: UpdateAccountIn,
    user: User = Depends(get_current_user),
    account_service: AccountService = Depends(AccountService),
):
    """
    Endpoint para atualizar uma conta.\n
    Algumas informações não podem ser atualizadas, como por exemplo o CPF.\n
    Somente o dono da conta pode atualizar as informações.
    """
    account_service.update(id, update_account_in, user.id)

    return {
        'message': 'Conta atualizada com sucesso.',
    }


@account_router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def deactivate_account(
    id: int,
    user: User = Depends(get_current_user),
    account_service: AccountService = Depends(AccountService),
):
    """
    Endpoint para desativar uma conta.\n
    Somente o dono da conta pode desativar.
    """
    account_service.deactivate(id, user.id)

    return {
        'message': 'Conta bloqueada com sucesso.',
    }
