import os
import re

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import rc

from palettable.colorbrewer.diverging import Spectral_10 as clrs
from palettable.colorbrewer.sequential import Blues_9 as blues
from palettable.colorbrewer.sequential import Reds_9 as reds


class SummaryTools():
    FY_OFFSET = -6

    def fy_series(df):
        return pd.DatetimeIndex(df['date']
               ).shift(SummaryTools.FY_OFFSET, freq='m'
               ).year

    def fy_filter(df, fy):
        return SummaryTools.fy_series(df) == fy

    def test_for_missing_groups(df, groups):
        for a in ('Income', 'Expenses'):
            filtered = pd.notnull(df[a])
            for project in df[filtered]['Project Codes'].unique():
                if not (project in groups[a]):
                    print(a, project, project in groups[a])

    def fy_summary(df):
        by_year = df.groupby(SummaryTools.fy_series(df))
        summary = by_year.sum()
        summary['Balance'] = by_year.apply(
            lambda ser: ser.iloc[-1,]
        )['Balance']
        return summary

    def project_summary(df):
        return df.groupby(df['Project Codes']).sum()

    def dollar_formatter(x):
        return '${:,.0f}'.format(x)

    def make_formatters():
        return {
            'Expenses': SummaryTools.dollar_formatter,
            'Income': SummaryTools.dollar_formatter,
        }

    def make_groups_filter_fn(df, groups):
        def fn(i):
            g = groups[df.loc[i, 'Project Codes']]
            if g == 'ERRORS':
                print(df.loc[i])
                print(groups[df.loc[i, 'Project Codes']])
                raise ValueError(df.loc[i])
            return g
        return fn


    def pretty_summary(df, groups, fy):
        df = df[~ df['Internal']]
        df = df[SummaryTools.fy_filter(df, fy)]

        summaries = []
        for i in groups:
            df_i = df[pd.notnull(df[i])]
            fn = SummaryTools.make_groups_filter_fn(df_i, groups[i])
            summaries += [(i, df_i.groupby(fn).sum()[i])]

        return summaries


    def pie_chart(df, field):
        labels = [
            ('%.1f%% - ' % (df.loc[a, field] / df.sum() * 100) + re.sub(r'-', ' ', a))
            for a in df.index
        ]

        if field == 'Expenses':
            cmap = reds
            df['Expenses'] = df['Expenses'] * -1
        elif field == 'Income':
            cmap = blues
        else:
            raise ValueError(field)

        fig = plt.figure(figsize=(10, 6), constrained_layout=False)
        ax = fig.add_axes([0,0,1,1])
        plt.subplots_adjust(0,0,1,1)
        colours = cmap.hex_colors
        img, texts = plt.pie(
            df.values[:, 0],
            labels=labels,
            center=(0, 0),
            colors=colours,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        [t.set_fontsize(12) for t in texts]

        # if field == 'Expenses':
        #     plt.arrow(1.08, 0.03, -0.04, 0.0, head_width=0.025, head_length=0.02)

        p=plt.gcf()
        p.gca().add_artist(plt.Circle((0,0), 0.6, color='white'))
