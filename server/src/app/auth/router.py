from fastapi import APIRouter, Depends
from core.security import get_current_user
from app.auth.schemas import TokenIn, TokenOut
from app.auth.models import User
from app.auth.service import AuthService


auth_router = APIRouter(tags=['Auth'], prefix='/api')


@auth_router.post('/login')
def login(
    token_in: TokenIn, auth_service: AuthService = Depends(AuthService)
) -> TokenOut:
    """
    Endpoint para realização do login.\n
    Recebe o cpf do dono da conta e a senha de acesso.\n
    Retorna o token JWT.
    """
    token: str = auth_service.login(token_in)
    return TokenOut(accessToken=token)


@auth_router.delete('/logout')
def logout(
    user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(AuthService),
):
    """
    Endpoint para deslogar o usuário.\n
    Remove o token JWT do banco de dados
    """
    auth_service.logout(user)
    return {
        'message': 'Conta desconectada com sucesso.',
        'detail': {'user': {'id': user.id, 'nome': user.account.person.name}},
    }
