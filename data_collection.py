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


