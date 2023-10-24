import os
import pandas as pd


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
co2_df = pd.read_json(CURR_DIR_PATH+'\\data_sets\\air_quality\\owid-co2-data.json')

who_pm25df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\air_quality\\WHO_world_pm25_pollution.csv')


mean_pm25 = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\air_quality\\mean_pm25.csv')
mean_pm25.rename(columns={'Country': 'Location'}, inplace=True)

# Health dataframes
death_rates_1990_2019df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\health\\death-rates-from-air-pollution.csv')
death_factor_1990_2019df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\health\\number-of-deaths-by-risk-factor.csv')
disease_factor_1990_2019df = pd.read_csv(CURR_DIR_PATH+'\\data_sets\\health\\disease-burden-by-risk-factor.csv')

# Clean-up
who_columns_delete = list(range(0,7)) + list(range(8,9)) + list(range(10,23))+ list(range(24,29))+ list(range(30,34))
who_pm25df.drop(who_pm25df.columns[who_columns_delete], axis=1, inplace=True)
who_pm25df.rename(columns={'Period': 'Year'}, inplace=True)
who_pm25df['Location'].replace({'Bolivia (Plurinational State of)': 'Bolivia'}, inplace=True)
who_pm25df['Location'].replace({'Brunei Darussalam': 'Brunei'}, inplace=True)
who_pm25df['Location'].replace({'Cabo Verde': 'Cape Verde'}, inplace=True)
who_pm25df['Location'].replace({'Côte d’Ivoire': "Cote d'Ivoire"}, inplace=True)
who_pm25df['Location'].replace({'Democratic Republic of the Congo': 'Democratic Republic of Congo'}, inplace=True)
who_pm25df['Location'].replace({"Democratic People's Republic of Korea": 'North Korea'}, inplace=True)
who_pm25df['Location'].replace({'Iran (Islamic Republic of)': 'Iran'}, inplace=True)
who_pm25df['Location'].replace({"Lao People's Democratic Republic": 'Laos'}, inplace=True)
who_pm25df['Location'].replace({'Micronesia (Federated States of)': 'Micronesia (country)'}, inplace=True)
who_pm25df['Location'].replace({'The former Yugoslav Republic of Macedonia': 'North Macedonia'}, inplace=True)
who_pm25df['Location'].replace({'Timor-Leste': 'East Timor'}, inplace=True)
who_pm25df['Location'].replace({'Türkiye': 'Turkey'}, inplace=True)
who_pm25df['Location'].replace({'Republic of Moldova': 'Moldova'}, inplace=True)
who_pm25df['Location'].replace({'Syrian Arab Republic': 'Syria'}, inplace=True)
who_pm25df['Location'].replace({"Republic of Korea": 'South Korea'}, inplace=True)
who_pm25df['Location'].replace({"Russian Federation": 'Russia'}, inplace=True)
who_pm25df['Location'].replace({"Occupied Palestinian territory": 'Palestine'}, inplace=True)
who_pm25df['Location'].replace({'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom'}, inplace=True)
who_pm25df['Location'].replace({'United States of America': 'United States'}, inplace=True)
who_pm25df['Location'].replace({'United Republic of Tanzania': 'Tanzania'}, inplace=True)
who_pm25df['Location'].replace({'Venezuela (Bolivarian Republic of)': 'Venezuela'}, inplace=True)
who_pm25df['Location'].replace({'Viet Nam': 'Vietnam'}, inplace=True)
who_pm25df.sort_values(by=['Location', 'Year'], inplace=True)
one_value_per_year = who_pm25df.groupby(['Location', 'Year'])['FactValueNumeric'].idxmax()
who_pm25df = who_pm25df.loc[one_value_per_year]
who_pm25df.to_csv(CURR_DIR_PATH+'\\data_sets\\air_quality\\who_pm_df.csv', index=False)


death_factor_columns_delete = list(range(3,14)) + list(range(15,18))+ list(range(19,27))+ list(range(28,31))
death_factor_1990_2019df.drop(death_factor_1990_2019df.columns[death_factor_columns_delete], axis=1, inplace=True)

disease_factor_columns_delete = list(range(3,5)) + list(range(6,18))+ list(range(19,24))
disease_factor_1990_2019df.drop(disease_factor_1990_2019df.columns[disease_factor_columns_delete], axis=1, inplace=True)

merged_df = death_rates_1990_2019df.merge(death_factor_1990_2019df, on=['Entity', 'Code', 'Year'], how='inner')
merged_df = merged_df.merge(disease_factor_1990_2019df, on=['Entity', 'Code', 'Year'], how='inner')

merged_df.rename(columns={'Entity': 'Location'}, inplace=True)
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

health_df = merged_df[(merged_df['Year'] >= 2010) & (merged_df['Year'] <= 2019)]
health_df.to_csv(CURR_DIR_PATH+'\\data_sets\\health\\health_df.csv', index=False)

health_df = health_df[health_df['Location'] != 'African Region (WHO)']
health_df = health_df[health_df['Location'] != 'American Samoa']
health_df = health_df[health_df['Location'] != 'Bermuda']
health_df = health_df[health_df['Location'] != 'East Asia & Pacific (WB)']
health_df = health_df[health_df['Location'] != 'Greenland']
# health_df = health_df[health_df['Location'] != 'East Timor']
health_df = health_df[health_df['Location'] != 'Eastern Mediterranean Region (WHO)']
health_df = health_df[health_df['Location'] != 'England']
health_df = health_df[health_df['Location'] != 'Europe & Central Asia (WB)']
health_df = health_df[health_df['Location'] != 'European Region (WHO)']
health_df = health_df[health_df['Location'] != 'G20']
health_df = health_df[health_df['Location'] != 'Guam']
health_df = health_df[health_df['Location'] != 'High Income (WB)']
health_df = health_df[health_df['Location'] != 'Latin America & Caribbean (WB)']
health_df = health_df[health_df['Location'] != 'Low Income (WB)']
health_df = health_df[health_df['Location'] != 'Lower Middle Income (WB)']
health_df = health_df[health_df['Location'] != 'Middle East & North Africa (WB)']
health_df = health_df[health_df['Location'] != 'Middle Income (WB)']
health_df = health_df[health_df['Location'] != 'North America (WB)']
health_df = health_df[health_df['Location'] != 'Northern Ireland']
health_df = health_df[health_df['Location'] != 'OECD Countries']
health_df = health_df[health_df['Location'] != 'Northern Mariana Islands']
health_df = health_df[health_df['Location'] != 'Puerto Rico']
health_df = health_df[health_df['Location'] != 'Region of the Americas (WHO)']
health_df = health_df[health_df['Location'] != 'Sub-Saharan Africa (WB)']
health_df = health_df[health_df['Location'] != 'South-East Asia Region (WHO)']
health_df = health_df[health_df['Location'] != 'South Asia (WB)']
health_df = health_df[health_df['Location'] != 'Scotland']
health_df = health_df[health_df['Location'] != 'Taiwan']
health_df = health_df[health_df['Location'] != 'Tokelau']
health_df = health_df[health_df['Location'] != 'United States Virgin Islands']
health_df = health_df[health_df['Location'] != 'Western Pacific Region (WHO)']
health_df = health_df[health_df['Location'] != 'World']
health_df = health_df[health_df['Location'] != 'Wales']

concatenated_df = pd.concat([health_df, who_pm25df])
irregularities = concatenated_df[concatenated_df.duplicated(subset='Location', keep=False)]

missing_in_df1 = health_df[~health_df['Location'].isin(who_pm25df['Location'])]
missing_in_df2 = who_pm25df[~who_pm25df['Location'].isin(health_df['Location'])]

# print(missing_in_df2)


print(health_df)
print(who_pm25df)