import pandas as pd
from sklearn.impute import KNNImputer
merge = pd.read_csv("data/merge.csv")

#Datetime 
merge['Datetime'] = pd.to_datetime(merge['Datetime'])

#Segmenting dataframes 

segments = merge.groupby(['Resolution'])

res_ten = segments.get_group('10MIN')
res_hour = segments.get_group('1H')
res_day = segments.get_group('D')

#TODO use KNN Imputer
# ten_imputer = KNNImputer(n_neighbors=5)
# res_ten = pd.DataFrame(ten_imputer.fit_transform(res_ten),columns ='Price')

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

res_ten = resample_two_hours(res_ten)
res_hour = resample_two_hours(res_hour)

def upsample_day(df):
    df = df.drop('Resolution',axis=1)
    df = df.set_index('Datetime')
    df = df.resample('120T').ffill()
    return df

res_day = upsample_day(res_day)





