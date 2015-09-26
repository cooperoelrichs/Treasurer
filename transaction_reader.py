import csv
from data_containers import Transaction, validate_transaction


class TransactionReader:
    def read_transactions(self, file_name):
        pass

    @staticmethod
    def read_csv(file_name):
        transactions = []
        with open(file_name) as f:  # newline='\n'
            csv_reader = csv.reader(f)  # , delimiter=' ')
            header = next(csv_reader)
            print(header)

            for row in csv_reader:
                # print(row)
                year = int(row[0])
                month = int(row[1])
                day = int(row[2])
                details = row[3]
                special = row[4]
                expense = TransactionReader.float_row(row, 5)
                income = TransactionReader.float_row(row, 6)
                transaction = Transaction(year, month, day, details, special, expense, income)

                if transaction.special == 'NOTE':
                    pass
                else:
                    validate_transaction(transaction)
                    transactions.append(transaction)
        return transactions

    @staticmethod
    def float_row(row, i):
        if row[i] == '':
            return None
        else:
            # return float(row[i].replace('.00', ''))
            return float(row[i].replace(',', ''))

    # def csv_writer
    #     with open(nlogit_dataset_file_name, 'w', newline='\n') as f:
    #         csv_writer = csv.writer(f)  # , delimiter=' ')
    #         # csv_writer.writerow(output_headers)
    #         for row in output_matrix:
    #             csv_writer.writerow([typeriser(i, x) for i, x in enumerate(row)])
