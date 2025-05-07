from app.transaction.schemas import (
    TransactionMonthResumeOut,
    TransactionMonthResumeNumericOut,
)


def create_year_transaction_resume_by_month(
    data: list[TransactionMonthResumeNumericOut],
):
    months = {
        1: 'Jan',
        2: 'Fev',
        3: 'Mar',
        4: 'Abr',
        5: 'Mai',
        6: 'Jun',
        7: 'Jul',
        8: 'Ago',
        9: 'Set',
        10: 'Out',
        11: 'Nov',
        12: 'Dez',
    }
    this_year_transactions_resume: list[dict] = []

    for _, value in months.items():
        this_year_transactions_resume.append({'month': value, 'label': 'Entrada'})
        this_year_transactions_resume.append({'month': value, 'label': 'Saída'})

    if len(data) == 0:
        return [
            TransactionMonthResumeOut(**result, amount=0)
            for result in this_year_transactions_resume
        ]

    for resume in data:
        for month_resume in this_year_transactions_resume:
            if months.get(resume.month) == month_resume.get(
                'month'
            ) and resume.label == month_resume.get('label'):
                month_resume['amount'] = resume.amount
            elif month_resume.get('amount') is None:
                month_resume['amount'] = 0

    return this_year_transactions_resume
