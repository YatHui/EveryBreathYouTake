# Cleaning dataset from WHO Annual Mean Air Particulates (PM2.5) with just total from each year for all countries
# 195 countries from 2010-2019

import pandas as pd
import country_converter as coco

df = pd.read_csv('data_sets/air_quality/WHO_,annual_mean_pm25.csv')


# Create a new dataframe with total annual values only

df_total = df
df_total = df.iloc[:, [0, 1, 6, 11, 16, 21, 26, 31, 36, 41, 46]]

# Rename column names
new_columns = ['Country','2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010' ]
df_total.columns = new_columns

# Drop top two rows
df_total = df_total.drop(df_total.index[[0,1]])

# Keep mean values only
columns_to_process = ['2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']

for col in columns_to_process:
    df_total[col] = df_total[col].str.extract(r'^([\d.]+)')

# Use country_converter to assign a Continent to a Country as a new column 
# pip install country_converter

cc = coco.CountryConverter()
df_total['continent'] = df_total['Country'].apply(lambda x: cc.convert(x, to='continent'))
df_total.insert(loc=1, column='Continent', value=df_total['continent'])
df_total = df_total.drop(columns=['continent'])

# Exporting to clean csv
df_total.to_csv('data_sets/air_quality/mean_pm25.csv', index=False)

# print(df_total)

