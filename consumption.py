import pandas as pd
from datetime import datetime
import seaborn as sns 
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

consumption_df = consumption_df.set_index(consumption_df['DayMonth'])

consumption_df.drop(columns=['Date','Consumption','Year','DayMonth'],axis=1,inplace=True)
consumption_df = consumption_df[0:366]

consumption_df['Min16-20'] = consumption_df[['2016','2017','2018','2019','2020']].min(axis=1)
consumption_df['Max16-20'] = consumption_df[['2016','2017','2018','2019','2020']].max(axis=1)
consumption_df['Avg16-20'] = consumption_df[['2016','2017','2018','2019','2020']].mean(axis=1)




fig, ax = plt.subplots(1, figsize=[14,4])


ax.fill_between(consumption_df.index, consumption_df["Min16-20"], consumption_df["Max16-20"], label="5y range", facecolor="oldlace")
ax.plot(consumption_df.index, consumption_df['2021'], label="2021", c="b")
ax.plot(consumption_df.index, consumption_df['2022'], label="2022", c="g")
ax.plot(consumption_df.index, consumption_df['Avg16-20'], label="Avg16-20", c="m")


ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.legend(loc = 'best')