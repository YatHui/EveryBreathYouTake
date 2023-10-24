# Cleaning dataset from WHO Annual Mean Air Particulates (PM2.5) with just total from each year for all countries
# 195 countries from 2010-2019

import pandas as pd

df = pd.read_csv('data_sets/air_quality/WHO_,annual_mean_pm25.csv')


# Create a new dataframe with total annual values only

df_total = df
df_total = df.iloc[:, [0, 1, 6, 11, 16, 21, 26, 31, 36, 41, 46]]

# Rename column names
new_columns = ['Countries, territories and aras','2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010' ]
df_total.columns = new_columns

# Drop top two rows
df_total = df_total.drop(df_total.index[[0,1]])

# Keep mean values only
columns_to_process = ['2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']

for col in columns_to_process:
    df_total[col] = df_total[col].str.extract(r'^([\d.]+)')

# Exporting to clean csv
df_total.to_csv('./data_sets/air_quality/mean_pm25.csv', index=False)

# print(df_total)

