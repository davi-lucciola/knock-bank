from validate_docbr import CPF
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


def validate_cpf(value: str) -> None:
    if CPF().validate(value) is False:
        raise ValueError('Cpf Inválido.')


def validate_password(value: str) -> None:
    if len(value) < 8:
        raise ValueError('A senha deve conter no minímo 8 caracteres.')

    have_lower = have_upper = have_digits = have_special = False
    for char in value:
        if char in ascii_lowercase:
            have_lower = True

        if char in ascii_uppercase:
            have_upper = True

        if char in digits:
            have_digits = True

        if char in punctuation:
            have_special = True

        if have_upper and have_digits and have_lower and have_special:
            break

    else:
        if have_lower is False:
            raise ValueError('A senha deve conter letras minúsculas.')

        if have_upper is False:
            raise ValueError('A senha deve conter letras maiúsculas.')

        if have_digits is False:
            raise ValueError('A senha deve conter numeros.')

        if have_special is False:
            raise ValueError('A senha deve conter caracteres especiais.')
