# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 18:00:07 2022

@author: a383785
"""
import pandas as pd
import numpy as np


df_qty = pd.read_csv('ds_gps.gps_quantity_per_period.csv')
df_price = pd.read_csv('ds_gps.gps_price_change.csv')
df_price['Min_Eff_Date'] = df_price['EFFECTIVE_DATE']

df_price[['Date','Month','Year']]=df_price.EFFECTIVE_DATE.str.split('/',expand=True)

df_qty[['Code','ITEM_NUMBER']]=df_qty.PART_KEY.str.split('|',expand=True)

df1 = df_qty.copy()

df1['Year_period'] = df1['PERIOD'].astype(str).str.slice(stop=4)

df1 = df1.groupby(['SUPPLIER_KEY','ITEM_NUMBER','Year_period']).agg({'ITEM_QUANTITY': 'sum'}).reset_index()

df1.columns = ['SUPPLIER_KEY','Item_Number','years','Quantity']


# convert the 'Date' column to datetime format
df_price['EFFECTIVE_DATE']= pd.to_datetime(df_price['EFFECTIVE_DATE'], format='%d/%m/%Y')
df_price['Min_Eff_Date']= pd.to_datetime(df_price['Min_Eff_Date'], format='%d/%m/%Y')

df2 = df_price.groupby(['ITEM_NUMBER','PREVIOUS_PRICE_AMOUNT']).agg({'EFFECTIVE_DATE': 'max','Min_Eff_Date':'min'})

df3 = df_price.groupby(['ITEM_NUMBER','PREVIOUS_PRICE_AMOUNT']).agg({'Year': ['max','min']}).reset_index()
df3.columns = ['Item_Number','Price','Max_year','Min_year']
# df3 = df3.melt(id_vars=['Item_Number','Price'], value_vars=['Max_year','Min_year'], ignore_index=False)

# change datatypes

df1 = df1.astype({
    'SUPPLIER_KEY': 'str',
    'Item_Number' : 'str',
    'years': 'int64',
    'Quantity': 'float16'
})

df3 = df3.astype({
    'Item_Number': 'str',
    'Price' : 'float16',
    'Min_year': 'int64',
    'Max_year': 'int64'
})

# df3.loc[df3["Min_year"] == df3['Max_year'] , "Max_year"] = 2022

#Fill the gap between min and max years
zipped = zip(df3['Item_Number'],df3['Price'], df3['Min_year'], df3['Max_year'])

# melting the max_year and min_year columns into 1 column
df = pd.DataFrame([(i,f, y) for i, f ,s, e in zipped for y in range(s, e+1)],
                   columns=['Item_Number','Price','years'])

df_final = pd.merge(df, df1, on = ['Item_Number','years'])

# df2['Days_number'] = df2['EFFECTIVE_DATE'] - df2['Min_Eff_Date']

df.info()


