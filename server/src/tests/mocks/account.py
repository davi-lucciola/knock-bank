from app.account.schemas import AccountIn, UpdateAccountIn


def create_account_in():
    return AccountIn(
        name='Davi',
        cpf='58901211033',
        accountType=1,
        birthDate='2004-01-14',
        password='Test#1234',
        dailyWithdrawLimit=1000,
    ).model_dump(mode='json')


def update_account_in():
    return UpdateAccountIn(
        name='Novo Nome', birthDate='2000-01-23', accountType=2, dailyWithdrawLimit=2000
    ).model_dump(mode='json')
