from collections import namedtuple

Transaction = namedtuple('Transaction', ['year', 'month', 'day', 'details', 'special', 'expense', 'income'])


def validate_transaction(transaction):
    not_none(transaction.year)
    not_none(transaction.month)
    not_none(transaction.day)
    expense_or_income(transaction)
    is_positive_or_none(transaction.income)
    is_negative_or_none(transaction.expense)


def is_positive_or_none(x):
    if x is None:
        pass
    elif x <= 0:
        raise(ValueError('Is not positive'))


def is_negative_or_none(x):
    if x is None:
        pass
    elif x >= 0:
        raise(ValueError('Is not negative'))


def expense_or_income(transaction):
    if transaction.expense is None and transaction.income is None:
        raise(ValueError('Not expense or transaction'))


def not_none(x):
    if x is None:
        raise(ValueError('is None'))
