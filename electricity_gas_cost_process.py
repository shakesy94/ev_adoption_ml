import pandas as pd
import numpy as np

df_zip_codes = pd.read_csv('TX_WA_CO_NY.csv')
df_dal = pd.read_csv('Dallas_electricity_gas_prices.csv')
df_hou = pd.read_csv('Houston_electricity_gas_prices.csv')
df_sea = pd.read_csv('Seattle_electricity_gas_prices.csv')
df_nyc = pd.read_csv('NYC_electricity_gas_prices.csv')
df_den = pd.read_csv('Denver_electricity_gas_prices.csv')
df_TX_elec_rural = pd.read_excel('sp_tx_electricity_price_summary.xls')
df_WA_elec_rural = pd.read_excel('sp_wa_electricity_price_summary.xls')
df_NY_elec_rural = pd.read_excel('sp_ny_electricity_price_summary.xls')
df_CO_elec_rural = pd.read_excel('sp_co_electricity_price_summary.xls')
df_TX_gas = pd.read_excel('eia_tx_gas_prices_summary.xls', sheet_name='Data 1')
df_WA_gas = pd.read_excel('eia_wa_gas_prices_summary.xls', sheet_name='Data 1')
df_NY_gas = pd.read_excel('eia_ny_gas_prices_summary.xls', sheet_name='Data 1')
df_CO_gas = pd.read_excel('eia_co_gas_prices_summary.xls', sheet_name='Data 1')

all_zip = df_zip_codes.iloc[:,0:2]
zip_dal = df_dal.iloc[:,6]
zip_hou = df_hou.iloc[:,6]
zip_sea = df_sea.iloc[:,6]
zip_nyc = df_nyc.iloc[:,6]
zip_den = df_den.iloc[:,6]

data_copy_dal = df_dal.iloc[0:50,0:6]
data_copy_hou = df_hou.iloc[0:50,0:6]
data_copy_sea = df_sea.iloc[0:50,0:6]
data_copy_nyc = df_nyc.iloc[0:50,0:6]
data_copy_den = df_den.iloc[0:50,0:6]

data_copy_TX_rural = df_TX_elec_rural.iloc[8:31,1:6].dropna(axis=1, how='all').dropna(how='any')
data_copy_TX_rural.rename(columns=data_copy_TX_rural.iloc[0], inplace = True) #turn first row into column header
data_copy_TX_rural.drop([8], inplace = True) #drop former row (now column header)
data_copy_TX_rural = data_copy_TX_rural.loc[~(data_copy_TX_rural==0).any(axis=1)] #remove 0s

data_copy_WA_rural = df_WA_elec_rural.iloc[8:40,1:6].dropna(axis=1, how='all').dropna(how='any')
data_copy_WA_rural.rename(columns=data_copy_WA_rural.iloc[0], inplace = True) #turn first row into column header
data_copy_WA_rural.drop([8], inplace = True) #drop former row (now column header)
data_copy_WA_rural = data_copy_WA_rural.loc[~(data_copy_WA_rural==0).any(axis=1)] #remove 0s

data_copy_NY_rural = df_NY_elec_rural.iloc[8:16,1:6].dropna(axis=1, how='all').dropna(how='any')
data_copy_NY_rural.rename(columns=data_copy_NY_rural.iloc[0], inplace = True) #turn first row into column header
data_copy_NY_rural.drop([8], inplace = True) #drop former row (now column header)
data_copy_NY_rural = data_copy_NY_rural.loc[~(data_copy_NY_rural==0).any(axis=1)] #remove 0s

data_copy_CO_rural = df_CO_elec_rural.iloc[8:22,1:6].dropna(axis=1, how='all').dropna(how='any')
data_copy_CO_rural.rename(columns=data_copy_CO_rural.iloc[0], inplace = True) #turn first row into column header
data_copy_CO_rural.drop([8], inplace = True) #drop former row (now column header)
data_copy_CO_rural = data_copy_CO_rural.loc[~(data_copy_CO_rural==0).any(axis=1)] #remove 0s

data_gas_TX_avg = df_TX_gas.iloc[2:,:]
data_gas_TX_avg.rename(columns={"Back to Contents": "Date", "Data 1: Texas Regular Conventional Retail Gasoline Prices (Dollars per Gallon)": "Gas Price"}, inplace = True)
data_gas_WA_avg = df_WA_gas.iloc[2:,:]
data_gas_WA_avg.rename(columns={"Back to Contents": "Date", "Data 1: Washington All Grades All Formulations Retail Gasoline Prices (Dollars per Gallon)": "Gas Price"}, inplace = True)
data_gas_NY_avg = df_NY_gas.iloc[2:,:]
data_gas_NY_avg.rename(columns={"Back to Contents": "Date", "Data 1: New York City Regular All Formulations Retail Gasoline Prices (Dollars per Gallon)": "Gas Price"}, inplace = True)
data_gas_CO_avg = df_CO_gas.iloc[2:,:]
data_gas_CO_avg.rename(columns={"Back to Contents": "Date", "Data 1: Colorado All Grades All Formulations Retail Gasoline Prices (Dollars per Gallon)": "Gas Price"}, inplace = True)

#print(data_gas_TX_avg.shape[0])
# Add year column to EIA gas prices dataframe - make sure each state has the same number of gas price entries (rows)
current_year = 2017
months = 12
month_count = 1
year_list = []
for i in range(data_gas_TX_avg.shape[0]):
    year_list.append(current_year)
    if month_count == 12:
        month_count = 0
        current_year += 1
    month_count += 1
data_gas_TX_avg['Year'] = year_list
data_gas_WA_avg['Year'] = year_list
data_gas_NY_avg['Year'] = year_list
data_gas_CO_avg['Year'] = year_list

print(data_gas_CO_avg.columns)

zip_code_list = all_zip.values[:,1].tolist()
zip_code_set = set(zip_code_list)
month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

rural_electricity_price_avg_TX = data_copy_TX_rural.mean(axis=0).round(2)
data_copy_TX_total = pd.concat([data_copy_dal, data_copy_hou]) #Add Dallas and Houston data before taking average for gas price
annual_gas_price_avg_TX = data_copy_TX_total.groupby('Year').mean().round(2)
rural_electricity_price_avg_WA = data_copy_WA_rural.mean(axis=0).round(2)

rural_electricity_price_avg_NY = data_copy_NY_rural.mean(axis=0).round(2)
rural_electricity_price_avg_CO = data_copy_CO_rural.mean(axis=0).round(2)

zip_state_dict = {}

for index, row_out in all_zip.iterrows():
    if row_out['ZIP Code'] in zip_state_dict.keys():
        None
    else:
        zip_state_dict[row_out['ZIP Code']] = row_out['State']

df_updated = pd.DataFrame(columns = ['State', 'Zip Code', 'Year', 'Month', 'Electricity Price', 'Gas Price'])

for key in zip_state_dict:
    year_count = 0
    gas_index_count = 0
    if zip_state_dict[key] == 'TX' and not key in zip_dal.values and not key in zip_hou.values:
        print(key)
        for (columnName, columnData) in rural_electricity_price_avg_TX.iteritems(): # Year loop - Iterate through each year
            year_count += 1
            for month in month_list:
                df_updated.loc[len(df_updated.index)] = ['TX', key, str(int(columnName)), month, columnData, data_gas_TX_avg['Gas Price'].iloc[gas_index_count]] #Need to find average gas price
                gas_index_count += 1

    elif zip_state_dict[key] == 'WA' and not key in zip_sea.values:
        for (columnName, columnData) in rural_electricity_price_avg_WA.iteritems(): # Year loop - Iterate through each year
            year_count += 1
            for month in month_list:
                df_updated.loc[len(df_updated.index)] = ['WA', key, str(int(columnName)), month, columnData, data_gas_WA_avg['Gas Price'].iloc[gas_index_count]] #Need to find average gas price

    elif zip_state_dict[key] == 'NY' and not key in zip_nyc.values:
        for (columnName, columnData) in rural_electricity_price_avg_NY.iteritems(): # Year loop - Iterate through each year
            year_count += 1
            for month in month_list:
                df_updated.loc[len(df_updated.index)] = ['NY', key, str(int(columnName)), month, columnData, data_gas_NY_avg['Gas Price'].iloc[gas_index_count]] #Need to find average gas price
        
    elif zip_state_dict[key] == 'CO' and not key in zip_den.values:
        for (columnName, columnData) in rural_electricity_price_avg_CO.iteritems(): # Year loop - Iterate through each year
            year_count += 1
            for month in month_list:
                df_updated.loc[len(df_updated.index)] = ['CO', key, str(int(columnName)), month, columnData, data_gas_CO_avg['Gas Price'].iloc[gas_index_count]] #Need to find average gas price        

for zip in zip_dal:
    for index, row_out in data_copy_hou.iterrows():
        df_updated.loc[len(df_updated.index)] = ['TX', zip, row_out['Year'], row_out['Month'], row_out['Electricity Price'], row_out['Gas Price']]
for zip in zip_dal:
    for index, row_out in data_copy_dal.iterrows():
        df_updated.loc[len(df_updated.index)] = ['TX', zip, row_out['Year'], row_out['Month'], row_out['Electricity Price'], row_out['Gas Price']]
for zip in zip_sea:
    for index, row_out in data_copy_sea.iterrows():
        df_updated.loc[len(df_updated.index)] = ['WA', zip, row_out['Year'], row_out['Month'], row_out['Electricity Price'], row_out['Gas Price']]
for zip in zip_nyc:
    for index, row_out in data_copy_nyc.iterrows():
        df_updated.loc[len(df_updated.index)] = ['NY', zip, row_out['Year'], row_out['Month'], row_out['Electricity Price'], row_out['Gas Price']]  
for zip in zip_den:
    for index, row_out in data_copy_den.iterrows():
        df_updated.loc[len(df_updated.index)] = ['CO', zip, row_out['Year'], row_out['Month'], row_out['Electricity Price'], row_out['Gas Price']]


df_updated.to_csv('electricity_gas_prices_updated.csv')


