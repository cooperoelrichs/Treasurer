

class TransactionProcessor(object):
    def __init__(self, transactions):
        self.transactions = transactions
        self.starting_balance = self.get_starting_balance()

    def income(self):
        return self.column_total(self.transactions, 'income')

    def expenses(self):
        return self.column_total(self.transactions, 'expense')

    @staticmethod
    def column_total(transactions, field):
        transactions = [x for x in transactions if x.special != 'Balance']
        values = [getattr(x, field) for x in transactions if getattr(x, field) is not None]
        return sum(values)

    def balance(self):
        return self.starting_balance + self.income() + self.expenses()

    def get_starting_balance(self):
        balances = [x for x in self.transactions if x.special == 'Balance']
        if len(balances) > 1:
            raise(RuntimeError('Too many balance transactions'))
        balance = balances[0]
        return balance.income
