import os
import pandas as pd


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
co2_df = pd.read_json(CURR_DIR_PATH+'\\data_sets\\air_quality\\owid-co2-data.json')

who_pm25df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\air_quality\\WHO_world_pm25_pollution.csv')

# Health dataframes
death_rates_1990_2019df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\health\\death-rates-from-air-pollution.csv')
death_factor_1990_2019df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\health\\number-of-deaths-by-risk-factor.csv')
disease_factor_1990_2019df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\health\\disease-burden-by-risk-factor.csv')

# Clean-up
who_columns_delete = list(range(0,7)) + list(range(8,9)) + list(range(10,23))+ list(range(24,29))+ list(range(30,34))
who_pm25df.drop(who_pm25df.columns[who_columns_delete], axis=1, inplace=True)

death_factor_columns_delete = list(range(3,14)) + list(range(15,18))+ list(range(19,27))+ list(range(28,31))
death_factor_1990_2019df.drop(death_factor_1990_2019df.columns[death_factor_columns_delete], axis=1, inplace=True)

disease_factor_columns_delete = list(range(3,5)) + list(range(6,18))+ list(range(19,24))
disease_factor_1990_2019df.drop(disease_factor_1990_2019df.columns[disease_factor_columns_delete], axis=1, inplace=True)

merged_df = death_rates_1990_2019df.merge(death_factor_1990_2019df, on=['Entity', 'Code', 'Year'], how='inner')
merged_df = merged_df.merge(disease_factor_1990_2019df, on=['Entity', 'Code', 'Year'], how='inner')

merged_df.rename(columns={'Deaths that are from all causes attributed to household air pollution from solid fuels per 100,000 people, in both sexes aged age-standardized': 'Death from household air pollution from solid fuels'}, inplace=True)
merged_df.rename(columns={'Deaths that are from all causes attributed to ambient particulate matter pollution per 100,000 people, in both sexes aged age-standardized': 'Death from ambient particulate matter pollution'}, inplace=True)
merged_df.rename(columns={'Deaths that are from all causes attributed to air pollution per 100,000 people, in both sexes aged age-standardized': 'Death from all causes attributed to air pollution'}, inplace=True)
merged_df.rename(columns={'Deaths that are from all causes attributed to ambient ozone pollution per 100,000 people, in both sexes aged age-standardized': 'Death from ambient ozone pollution'}, inplace=True)
merged_df.rename(columns={'Deaths that are from all causes attributed to household air pollution from solid fuels, in both sexes aged all ages': 'Death from household air pollution from solid fuels (all ages)'}, inplace=True)
merged_df.rename(columns={'Deaths that are from all causes attributed to air pollution, in both sexes aged all ages': 'Death from attributed to air pollution (all ages)'}, inplace=True)
merged_df.rename(columns={'DALYs that are from all causes attributed to household air pollution from solid fuels, in both sexes aged all ages': 'DAILY causes attributed to household air pollution (all ages)'}, inplace=True)
merged_df.rename(columns={'DALYs that are from all causes attributed to ambient particulate matter pollution, in both sexes aged all ages': ' DAILY ambient particulate matter pollution (all ages)'}, inplace=True)
merged_df.rename(columns={'DALYs that are from all causes attributed to air pollution, in both sexes aged all ages': 'DAILY attributed to air pollution(all ages)'}, inplace=True)
merged_df.rename(columns={'Deaths that are from all causes attributed to ambient particulate matter pollution, in both sexes aged all ages': 'ambient particulate matter pollution(all ages)'}, inplace=True)

df = merged_df[(merged_df['Year'] >= 2010) & (merged_df['Year'] <= 2019)]
