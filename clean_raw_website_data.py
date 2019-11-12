# Import libraries
import pandas as pd
import os
import numpy as np

# Get raw file list
folder = 'data/raw/website'
file_list = os.listdir(folder)
file_list = [folder + '/' + x for x in file_list]

# Functions
def get_header_row(df):
    """
    For a csv or Excel file, it looks through each row starting from the 
    top to see which row has no null or missing values. This is useful 
    in determining the row that is the headerThis row is assumed to be 
    the row that 
    
    Dependencies: pandas, numpy
    
    Returns: an integer which indicates the row number of the header, or None 
    if such a row cannot be found
    """
    row = 0
    for row in range(len(df)):
        if np.nan in df.values.tolist()[row] or '' in df.values.tolist()[row]:
            row += 1
        else:
            return row
    return

# Collate all raw data files
all_data_list = []
for file in file_list:
    data = pd.read_excel(file, header=None)
    header_row = get_header_row(data)
    data = pd.read_excel(file, header=header_row)
    data['Source'] = file
    all_data_list.append(data)
all_data = pd.concat(all_data_list, axis=0, sort=False)
all_data = all_data.reset_index().drop('index', axis=1)

# Convert dates from string to date format
all_data['cleaned_date'] = pd.to_datetime(all_data['PriceUpdatedDate'])

# Change date formats for specific files that have converted the date incorrectly
wrong_date_files = ['data/raw/website/price_history_jun_2019.xlsx',
                    'data/raw/website/price_history_apr_2019.xlsx',
                    'data/raw/website/price_history_mar_2019.xlsx',
                    'data/raw/website/price_history_feb_2019.xlsx',
                    'data/raw/website/price_history_may_2019.xlsx',]
for source in wrong_date_files:
    source_rows = all_data['Source'] == source
    all_data.loc[source_rows, 'cleaned_date'] = pd.to_datetime(all_data.loc[source_rows, 'PriceUpdatedDate'], format='%d/%m/%Y %H:%M:%S %p')

# Remove rows that are entirely blank
subset = list(all_data.columns)
subset.remove('Source')
all_data = all_data.dropna(how='all', subset=subset)

# Remove duplicate rows
all_data = all_data.drop_duplicates()

# From the results, it was determine that files from Feb 2019 onwards had missing values

# We can see that these values need to be forward filled across service station name, address, suburb, postcode and Brand
ffill_columns = ['ServiceStationName', 'Address', 'Suburb', 'Postcode', 'Brand', 'FuelCode', 'PriceUpdatedDate', 'cleaned_date']

ffill_files = ['data/raw/website/price_history_may_2019.xlsx',
               'data/raw/website/price_history_jun_2019.xlsx',
               'data/raw/website/price_history_feb_2019.xlsx',
               'data/raw/website/price_history_apr_2019.xlsx',
               'data/raw/website/price_history_mar_2019.xlsx',]
ffill_source = all_data['Source'].isin(ffill_files)
all_data.loc[ffill_source, ffill_columns] = all_data.loc[ffill_source, ffill_columns].fillna(method='ffill')

# FuelCode and FuelType refer to the same type of data. Therefore we will fill in the values of FuelCode with FuelType
all_data['FuelCode'] = all_data['FuelCode'].fillna(all_data['FuelType'])
all_data = all_data.drop('FuelType', axis=1)

# There are some data points that are missing on both FuelCode and FuelType. This will be left as null values.
# Stations can have multiple fuel types being sold so it's not possible to infer the FuelCode from the station

# There is one row where the ServiceStationName is invalid as it is a grand total row
invalid_row = all_data[all_data['ServiceStationName'] == 'Rows 1 - 82817 (All Rows)'].index[0]
all_data = all_data.drop(invalid_row)

# There are some prices that are 10,000. These will be labelled as null
all_data.loc[all_data['Price'] == 10000, 'Price'] = np.nan

# There are a lot of prices that are labelled above 300 which are significant outliers.
all_data.loc[all_data['Price'] > 300, 'Price'] = np.nan

# Export the data
all_data.to_csv('data/interim/website_data.csv', index=False)