import pandas as pd

merge = pd.read_csv("data/merge.csv")

#Datetime 
merge['Datetime'] = pd.to_datetime(merge['Datetime'])

#Segmenting dataframes 

segments = merge.groupby(['Resolution'])

res_ten = segments.get_group('10MIN')
res_hour = segments.get_group('1H')
res_day = segments.get_group('D')


def fill_na_mean(df):
    mean_value = df['Price'].mean()
    df['Price'].fillna(value=mean_value,inplace=True)
    return df

res_ten = fill_na_mean(res_ten)
res_hour = fill_na_mean(res_hour)
res_day = fill_na_mean(res_day)

def resample_two_hours(df,way):
    df = df.drop('Resolution',axis=1)
    df = df.set_index('Datetime')
    if way == 'mean_val':
        df = df.resample('120T').mean()

    else:
        df = df.resample('120T').ffill()


    return df

res_ten = resample_two_hours(res_ten,'mean_val')
res_hour = resample_two_hours(res_hour,'mean_val')

def upsample_day(df):
    df = df.drop('Resolution',axis=1)
    df = df.set_index('Datetime')
    df = df.resample('120T').ffill()
    return df

res_day = upsample_day(res_day)

def filter_hours(df):
    df = df.reset_index()
    filt = (df['Datetime'].dt.hour >= 7) & (df['Datetime'].dt.hour <= 17)

    df_filtered = df.loc[filt, :]

    return df_filtered

filtered_res_hour = filter_hours(res_hour)
filtered_res_day = filter_hours(res_day)
filtered_res_ten = filter_hours(res_ten)

filtered_res_hour.rename(columns={'Price':'Hourly_Price'},inplace=True)
filtered_res_day.rename(columns={'Price':'Day_Price'},inplace=True)
filtered_res_ten.rename(columns={'Price':'TenMin_Price'},inplace=True)

filt_df = filtered_res_ten.merge(filtered_res_hour,on='Datetime', how = 'left')
final_df = filt_df.merge(filtered_res_day,on = 'Datetime', how= 'left')




final_df.to_csv("data/new_merged.csv")