import pandas as pd
import numpy as np
trades = pd.read_csv("data/Trades.csv")

#Datetime 
trades['TradeDateTime'] = pd.to_datetime(trades['TradeDateTime'])

# Replace values of columns by using DataFrame.loc[] property.
trades.loc[trades['Product'] == 'Emission - Venue B', 'Product'] = 'Emission - Venue A'


def get_interval(trades_df,day):
    """The dataframe has four days, specify
    which of the four days we are intertested in """
    df_by_date = trades_df.groupby([trades_df['TradeDateTime'].dt.date])

    all_dates = trades_df['TradeDateTime'].dt.date
    all_dates = np.array(all_dates.tolist())
    unique_dates = np.unique(all_dates)

    df_interval = df_by_date.get_group(unique_dates[day-1])
    
    return df_interval

def get_product(df,product):
    product_ohlc = {}
    product_segments = df.groupby(df['Product'])
    product_df = product_segments.get_group(product)

    contract_segments = product_df.groupby(product_df['Contract'])
    contracts = list(set(product_df['Contract'].tolist()))

    for contract in contracts:
        ohlc =  []
        contract_df = contract_segments.get_group(contract)
        all_prices = contract_df['Price'].tolist()
        high ,low = max(all_prices) , min(all_prices)
        ohlc.append(contract_df.iloc[0]['Price']) #open
        ohlc.append(high)
        ohlc.append(low)
        ohlc.append(contract_df.iloc[len(contract_df)-1]['Price']) #close

        product_ohlc[contract] = ohlc

    # open = product_df.iloc[0]['Price']
    # close = product_df.iloc[len(product_df)-1]['Price']
    # all_prices = product_df['Price'].tolist()
    # high ,low = max(all_prices) , min(all_prices)

    return product_ohlc

# TODO for each contract return ohlc

def main_func(df,day,begin,end,product,freq):
    product_ohlc = {}
    product_segments = df.groupby(df['Product'])
    product_df = product_segments.get_group(product)

    contract_segments = product_df.groupby(product_df['Contract'])
    contracts = list(set(product_df['Contract'].tolist()))

    for contract in contracts:
        contract_df = contract_segments.get_group(contract)
        contract_df = contract_df.set_index('Datetime')



