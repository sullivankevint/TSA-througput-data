"""
Script to clean data in csv format from TSA throghput data as found at https://www.tsa.gov/foia/readingroom

Data is converted to CSV using Tabula and then manually adjusted to ensure column heights are correct

Author: Kevin Sullivan
"""

import pandas as pd
import math
from checkpoints import checkpoints


filename = input('Please enter file name to clean: ')

df = pd.read_csv(filename, header = None)

#sometimes there is a dummy column at the end
if len(df.columns) == 8:
    df.columns = ['date', 'hour', 'iata_code', 'airport_name', 'city', 'state', 'checkpoint', 'passengers']
    df.drop(['airport_name', 'city', 'state'], axis = 1, inplace = True)
elif len(df.columns) == 9:
    df.columns = ['date', 'hour', 'iata_code', 'airport_name', 'city', 'state', 'checkpoint', 'passengers', 'null']
    df.drop(['airport_name', 'city', 'state', 'null'], axis = 1, inplace = True)
else:
    raise ValueError('Unexpected number of columns')

#for i in range(200):
#    print(pd.isnull(df.hour[i]))
##loop to fill in dates and hours until the IATA code cycles back as they are listed alphabetically

for i in range(len(df)-1):
    if not pd.isnull(df.iata_code[i]) and pd.isnull(df.iata_code[i+1]):
       if (df.checkpoint[i+1] in checkpoints[df.iata_code[i]]): #must used nested ifs to validate df.iata_code[i] is not null
           df.iata_code[i+1] = df.iata_code[i]

df.iata_code.fillna(method = 'bfill', inplace = True)

df.dropna(subset = ['passengers'], inplace = True)
df.reset_index(inplace = True)
df.drop(['index'], axis = 1, inplace = True)

for i in range(len(df)-1):
    if not pd.isnull(df.hour[i]) and pd.isnull(df.hour[i+1]) and (df.iata_code[i] <= df.iata_code[i+1]):
        df.hour[i+1] = df.hour[i]
    if not pd.isnull(df.date[i]) and pd.isnull(df.date[i+1]) and (df.iata_code[i] <= df.iata_code[i+1]):
        df.date[i+1] = df.date[i]



df.fillna(method = 'bfill', inplace = True)

clean_filename = filename[:-4] + '_clean.csv'
df.to_csv(clean_filename)

