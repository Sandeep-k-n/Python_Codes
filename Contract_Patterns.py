# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 15:05:45 2021

@author: a383785
"""
import json
import pandas as pd
import numpy as np

# Opening JSON file
f = open('Contract_Patterns_20210920-120708.json',)
 
# returns JSON object as
# a dictionary
data = json.load(f)

# Create dataframes
df = pd.DataFrame()

# Iterating through the json
# list
for i in data:
    df = df.append(i,ignore_index=True)
        
df1 = df['Parma'].str.split("#",expand=True)

length = len(df1.columns) - 1
# using while loop        
while(length >= 0):
      
    # checking condition
    if length % 2 != 0:
        df1.drop(df1.columns[(length-1)], axis=1, inplace=True)
      
    # increment i  
    length -= 2
    
length = len(df1.columns)
df1['Parma'] = "" 
while(length > 1):
    n = df1[df1.columns[0]]
    n.fillna("",inplace=True)
    df1['Parma'] = df1['Parma'] + n
    df1 = df1.drop(df1.columns[[0]], axis = 1)
    length = len(df1.columns)

df['Parma'] = df1['Parma'] 

def process(column, ident):
    df2 = df.drop(column, axis=1)\
              .join(df[column]
              .str
              .split(ident,expand=True)
              .stack()
              .reset_index(drop=True, level=1)
              .rename(column)           
              )
    return df2

process('Parma', ';')

#Split and stack columns : Parma, Segment Code, RM commodity
df2 = df.drop('Parma', axis=1)\
              .join(df['Parma']
              .str
              .split(';',expand=True)
              .stack()
              .reset_index(drop=True, level=1)
              .rename('Parma')           
              )

df2 = df2.drop('Segment Codes', axis=1)\
              .join(df['Segment Codes']
              .str
              .split('#',expand=True)
              .stack()
              .reset_index(drop=True, level=1)
              .rename('Segment Codes')           
              )
df2 = df2[df2['Segment Codes'].astype(str).str.match("[^\d;$].")]

df2 = df2.drop('RM Commodity', axis=1)\
              .join(df['RM Commodity']
              .str
              .split('#',expand=True)
              .stack()
              .reset_index(drop=True, level=1)
              .rename('RM Commodity')           
              )
              
df2 = df2[df2['RM Commodity'].astype(str).str.match("[^\d;$].")]
df3 = df2['RM Commodity'].str.split(":",expand=True)
df3.columns = ['RM Parent', 'RM Code', 'Index', 'RM Info']

df2 = pd.concat([df2, df3], axis=1)
df2.drop(['RM_Commodity'], axis=1, inplace=True)

#save to CSV   
df2.to_csv('Contract_patterns.CSV')


