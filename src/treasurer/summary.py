import os
import re
import textwrap

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc


from palettable.colorbrewer.diverging import Spectral_10 as clrs
from palettable.colorbrewer.sequential import Blues_9 as blues
from palettable.colorbrewer.sequential import Reds_9 as reds


class SummaryTools():
    FY_OFFSET = -6
    LAST_FY_OF_THE_BALI_ACC = 2017

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

        SummaryTools.calculated_balance(summary)
        summary['Balance'] = SummaryTools.calculated_balance(summary)

        post_bali_filter = summary.index > SummaryTools.LAST_FY_OF_THE_BALI_ACC
        summary.loc[post_bali_filter, 'Balance'] = by_year.apply(
            lambda ser: ser.iloc[-1,]
        ).loc[post_bali_filter, 'Balance']
        return summary

    def calculated_balance(summary):
        years = summary.index.values
        balances = []
        prev_balance = 0
        for i, y in enumerate(years):
            balances += [
                prev_balance +
                summary['Income'][summary.index == y].sum() +
                summary['Expenses'][summary.index == y].sum()
            ]
            prev_balance = balances[-1]

        return balances

    def project_summary(df):
        return df.groupby(df['Project Codes']).sum()

    def dollar_formatter(x):
        return '${:,.0f}'.format(x)

    def make_formatters():
        return {
            'Income': SummaryTools.dollar_formatter,
            'Expenses': SummaryTools.dollar_formatter,
            'Balance': SummaryTools.dollar_formatter,
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


    def pie_chart(df, field, img_dir, arrows):
        fig_size = 4
        v_margin = -0.1
        h_margin = 1.8

        labels = [
            # '%.1f%% - ' % (df.loc[a, field] / df.sum() * 100) + re.sub(r'-', ' ', a))
            textwrap.fill(re.sub(r'-', ' ', a), width=25)
            for a in df.index
        ]

        if field == 'Expenses':
            cmap = reds
            df['Expenses'] = df['Expenses'] * -1
        elif field == 'Income':
            cmap = blues
        else:
            raise ValueError(field)

        fig = plt.figure(
            facecolor=None, edgecolor=None, frameon=True,
            figsize=(fig_size, fig_size),
            constrained_layout=False,
            dpi=200
        )

        plt.subplots_adjust(0,0,1,1)

        colours = cmap.hex_colors
        _, texts = plt.pie(
            df.values[:, 0],
            labels=labels,
            # center=(0, 0),
            colors=colours,
            wedgeprops={'linewidth': 0.8, 'edgecolor': 'black'}
        )
        [t.set_fontsize(12) for t in texts]

        plt.gcf().gca().add_artist(plt.Circle(
            (0,0), 0.8, facecolor='lightgrey', edgecolor='black',
            linewidth=0.8)
        )

        if field in arrows:
            x, y, dx, dy = arrows[field]
            plt.arrow(x, y, dx, dy, head_width=0.03, head_length=0.03)

        bbox = mpl.transforms.Bbox([
            [-h_margin, -v_margin], [fig_size+h_margin, fig_size+v_margin]
        ])
        plt.savefig(
            fname=os.path.join(img_dir, '{}.png'.format(field)),
            bbox_inches=bbox,
        )
