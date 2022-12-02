import pandas as pd
from datetime import datetime

cons = pd.read_csv("data/Consumption.csv")

weird = '2020110'
d = datetime.strptime(weird, '%Y%m%d')
datetime_object = datetime.strptime(eg, '%d/%m/%Y')