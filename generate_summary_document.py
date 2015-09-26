from transaction_reader import TransactionReader
from transaction_processor import TransactionProcessor

bali_data = '/Users/cooperoelrichs/Documents/SIES/data/SIES transactions - Bali - Sheet1 - 2015-09-26.csv'
bangalow_data = '~/Documents/SIES/data/SIES transactions - Bangalow - Sheet1 - 2015-09-26.csv'

bali_transactions = TransactionReader.read_csv(bali_data)
bali_processor = TransactionProcessor(bali_transactions)

print(bali_processor.income())
print(bali_processor.expenses())
print(bali_processor.balance())
