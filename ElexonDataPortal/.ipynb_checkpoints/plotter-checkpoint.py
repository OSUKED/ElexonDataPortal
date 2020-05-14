## ~~~~~ Imports ~~~~~

## Data Manipulation
import pandas as pd
import numpy as np

## Plotting
import seaborn as sns
import matplotlib.pyplot as plt


## ~~~~~ Helper Functions & Variables ~~~~~

def hide_spines(ax, positions=['top', 'right']):
    """
    Pass a matplotlib axis and list of positions with spines to be removed
    
    args:
        ax:          Matplotlib axis object
        positions:   Python list e.g. ['top', 'bottom']
    """
    assert isinstance(positions, list), 'Position must be passed as a list '
    
    for position in positions:
        ax.spines[position].set_visible(False)

rgb_2_mpl = lambda rgb_tuple: tuple(rgb_val/250 for rgb_val in rgb_tuple)

general_colours = {
    'red' : rgb_2_mpl((140, 7, 0)),
    'yellow' : rgb_2_mpl((242, 203, 76)),
    'gold' : rgb_2_mpl((245, 158, 0)),
    'silver' : rgb_2_mpl((150, 150, 150)),
    'blue' : rgb_2_mpl((0, 0, 225))
}


## ~~~~~ Bid Offer Data ~~~~~

def plot_BOD_stack(df_imb_stack, title=''):
    plot_stack = lambda df_stack, ax, color='k': ax.fill_between(df_stack['volume'], 0, df_stack['price'], color=color, alpha=0.25)

    fig, ax = plt.subplots(dpi=150)

    plot_stack(df_imb_stack[df_imb_stack['volume']<=0], color=general_colours['red'], ax=ax)
    plot_stack(df_imb_stack[df_imb_stack['volume']>=0], color=general_colours['gold'], ax=ax)

    ax.plot([df_imb_stack['volume'].min(), df_imb_stack['volume'].max()], [0, 0], 'k--', lw=0.5)
    ax.plot([0, 0], [df_imb_stack['volume'].min()*1.1, df_imb_stack['volume'].max()], 'k--', lw=0.5)

    #hide_spines(ax)
    ax.set_xlim(df_imb_stack['volume'].min(), df_imb_stack['volume'].max())
    ax.set_ylim(df_imb_stack['price'].min()*1.1, df_imb_stack['price'].max())

    ax.set_ylabel('Net Cost to BM Unit (£/MWh)')
    ax.set_xlabel('Imbalance Adjustment Volume (MWh)', labelpad=10)
    
    ax.set_title(title)