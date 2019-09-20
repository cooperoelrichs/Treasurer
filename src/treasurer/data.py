import os

import numpy as np
import pandas as pd


class DataTools():
    def bool_conv(x, rules):
        if x in rules:
            return rules[x]
        else:
            raise ValueError('{} not valid input for a bool conversion'.format(x))

    def bool_conv_sparse(x):
        rules = {'TRUE': True, '': False}
        return DataTools.bool_conv(x, rules)

    def bool_conv_dense(x):
        rules = {'TRUE': True, 'FALSE': False}
        return DataTools.bool_conv(x, rules)

    def float_conv(x):
        if x == '':
            return np.nan
        else:
            return np.float(x.replace(",", ""))

    DTYPE_SPEC = {
        'Year': np.int32,
        'Month': np.int32,
        'Day': np.int32,
        'AUD - Expenses': np.float64,
        'AUD - Income': np.float64,
        'AUD - Balance': np.float64,
        # 'IDR - Expenses': np.float64,
        # 'IDR - Income': np.float64,
        # 'IDR - Account Balance': np.float64,
        'Project Codes': object,
        'Details': object,
        # 'Non-SIES': bool,
        # 'Via The SIES Account': bool,
        # 'Internal Transaction': bool,
    }

    CONVERTERS = {
        'Non-SIES': bool_conv_sparse,
        'Via The SIES Account': bool_conv_dense,
        'Internal Transaction': bool_conv_dense,
        'Internal': bool_conv_dense,
        'IDR - Expenses': float_conv,
        'IDR - Income': float_conv,
        'IDR - Account Balance': float_conv,
    }

    USE_COLS = set(DTYPE_SPEC.keys()).union(set(CONVERTERS.keys()))

    def load_data_file(dir_name, file_name):
        return pd.read_csv(
            os.path.join(dir_name, file_name),
            header=0, skiprows=(1,), thousands=',', decimal=b'.',
            usecols=lambda x: x in DataTools.USE_COLS,
            true_values=('TRUE'), false_values=('FALSE'),
            parse_dates={'date': ['Year', 'Month', 'Day']},
            dtype=DataTools.DTYPE_SPEC,
            converters=DataTools.CONVERTERS,
        )
