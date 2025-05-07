from enum import Enum


class AccountType(Enum):
    CURRENT_ACCOUNT = (1, 'Conta Corrente')
    SAVING_ACCOUNT = (2, 'Conta Poupança')
    SALARY_ACCOUNT = (3, 'Conta Salário')
    PAYMENT_ACCOUNT = (4, 'Conta Pagamento')

    @classmethod
    def get_account_type(cls, account_type_id: int):
        for account_type in cls:
            if account_type.value[0] == account_type_id:
                return account_type

        raise ValueError('Tipo de Conta Inválida.')
