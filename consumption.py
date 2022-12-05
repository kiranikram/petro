import pandas as pd
from datetime import datetime

cons = pd.read_csv("data/Consumption.csv")

#split df by Date type 
df1 = cons[0:1461]
df2 = cons[1461:1827]
df3 = cons [1827:2468]

df1['Date'] = pd.to_datetime(df1['Date'], format = '%d/%m/%Y')
df2['Date'] = pd.to_datetime(df2['Date'], format = '%Y%m%d')
df3['Date'] = pd.to_datetime(df3['Date'], format = '%d/%m/%Y')

consumption_df = pd.concat([df1,df2,df3],axis=0)

consumption_df['Year'] = consumption_df['Date'].dt.year

segments = consumption_df.groupby(['Year'])

years = list(set(consumption_df['Year'].tolist()))

def get_yearly_df(year):

    year_df = segments.get_group(year)
    year_df['DayMonth'] = year_df['Date'].dt.strftime("%d:%m")
    year_df.rename(columns ={'Consumption':str(year)},inplace = True)
    year_df.drop(columns=['Year','Date'],axis=1,inplace=True)

    return year_df


consumption_df['Date'] =  pd.to_datetime(consumption_df['Date'], format='%Y-%m-%d')

consumption_df['DayMonth'] = consumption_df['Date'].dt.strftime("%d:%m")

for year in years:

    yearly_df = get_yearly_df(year)

    consumption_df = consumption_df.merge(yearly_df,on='DayMonth',how='left')

consumption_df.drop(columns=['Date','Consumption','Year'],axis=1,inplace=True)
consumption_df = consumption_df[0:366]