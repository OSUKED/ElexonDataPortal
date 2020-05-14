## ~~~~~ Imports ~~~~~

## Data Manipulation
import pandas as pd
import numpy as np

## Plotting
import seaborn as sns
import matplotlib.pyplot as plt

## Stream Data
from ElexonDataPortal import stream_info


## ~~~~~ Bid Offer Data ~~~~~

def process_accepted_BOD_direction(df_accepted_BODs, direction='offer'):
    for col in [f'{direction}Price', f'{direction}Volume']:
        df_accepted_BODs[col] = df_accepted_BODs[col].astype(float)
        
    df_accepted_BOD_dir = (df_accepted_BODs
                           [['id', f'{direction}Price', f'{direction}Volume']]
                           .dropna()
                           .sort_values(f'{direction}Price')
                           .rename(columns={'id':'BMU_ID', f'{direction}Price':'price', f'{direction}Volume':'volume'})
                          )

    df_accepted_BOD_dir['cumulative_volume'] = df_accepted_BOD_dir['volume'].cumsum()
    
    if direction == 'bid':
        df_accepted_BOD_dir['price'] = -df_accepted_BOD_dir['price']
    
    return df_accepted_BOD_dir

def cum_vols_2_BOD_vol_stack(df_accepted_dir, shift_dir=1):
    price_stack_zipped_tuples = df_accepted_dir[['price', 'cumulative_volume']].itertuples(index=False, name=None)
    df_imb_stack = pd.DataFrame(sorted(list(price_stack_zipped_tuples)*2), columns=['price', 'volume'])

    df_imb_stack['volume'] = df_imb_stack['volume'].shift(shift_dir).fillna(0)
    df_imb_stack = (df_imb_stack
                    .sort_values(['volume', 'price'])
                    .reset_index(drop=True)
                   )
    
    if shift_dir == 1:
        df_imb_stack = pd.DataFrame({'price':[0], 'volume':[0]}).append(df_imb_stack)
    elif shift_dir == -1:
        df_imb_stack = df_imb_stack.append(pd.DataFrame({'price':[0], 'volume':[0]}))
    
    return df_imb_stack

def accepted_BODs_2_stack(df_accepted_BODs):   
    df_accepted_BODs = df_accepted_BODs[df_accepted_BODs['recordType'].isin(['OFFER', 'BID'])].copy()

    df_accepted_offers = process_accepted_BOD_direction(df_accepted_BODs, direction='offer')
    df_accepted_bids = process_accepted_BOD_direction(df_accepted_BODs, direction='bid')

    df_imb_stack_offers = cum_vols_2_BOD_vol_stack(df_accepted_offers, shift_dir=1)
    df_imb_stack_bids = cum_vols_2_BOD_vol_stack(df_accepted_bids, shift_dir=-1)

    df_imb_stack = df_imb_stack_bids.append(df_imb_stack_offers)
    
    return df_imb_stack