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


def main_func(df,day,product,freq,begin=7,end=17):
    """Args: df: original trades df,
            day: int(day out of working days provided)
            product: str(product name)
            freq: str(15T / 1H / 1D)
            begin: int(start of trading day)
            end: int(end of trading day)

       Returns: Dict of dataframes for time period specified. Each dataframe in the dictionary 
                corresponds to a unique contract for the product that is queried. 
    """
    df = get_interval(df,day)
    product_ohlc = {}
    product_segments = df.groupby(df['Product'])
    product_df = product_segments.get_group(product)

    contract_segments = product_df.groupby(product_df['Contract'])
    contracts = list(set(product_df['Contract'].tolist()))

    for contract in contracts:
        contract_df = contract_segments.get_group(contract)
        df = contract_df.set_index('TradeDateTime')
        open_df = df.resample(freq).agg({'Price': 'first'}) 
        high_df = df.resample(freq).agg({'Price': 'max'}) 
        low_df = df.resample(freq).agg({'Price': 'min'}) 
        close_df = df.resample(freq).agg({'Price': 'last'}) 
        volume_df = df.resample(freq).agg({'Price': 'sum'})
        con_df =pd.concat([open_df, high_df, low_df, close_df, volume_df], axis=1, keys=['open', 'high', 'low', 'close', 'volume'])
        if freq != '1D':
            df = con_df.reset_index()
            filt = (df['TradeDateTime'].dt.hour >= begin) & (df['TradeDateTime'].dt.hour <= end)

            con_df = df.loc[filt, :]

        con_df = con_df.dropna()

        product_ohlc[contract] = con_df

    return product_ohlc



