import pandas as pd
from datetime import time
import glob
import os

path_file = '/Users/joaopedrosantosmartins/Documents/Clients/Genesys/Requests/recordings_multi-oing_selection_20250724.csv' # use your path
output_file = "Geneysys_OTS_H2H_Breakdown Request.csv"
file_path_output = path_file.replace(path_file.split("/")[-1],output_file)
print(file_path_output)
df = pd.read_csv(path_file, index_col=None)

print(df)
df['Duration - Seconds'] = pd.DatetimeIndex(df['Duration']).minute
df['Duration - Mins'] = pd.DatetimeIndex(df['Duration']).hour
df['Total Duration - Mins'] = df['Duration - Mins'] + df['Duration - Seconds'].div(60)
df['Total Duration - Hours'] = df['Duration - Mins'].div(60) + df['Duration - Seconds'].div(60*60)

# df['Duration - Seconds'] = df['Duration'].dt.second

# total_hours = round(float(df['Duration - Seconds'].sum()/(60*60)),2)
print(df[['Duration','Duration - Seconds','Duration - Mins','Total Duration - Hours']])

dict_info = {
    "Locale": [], 
    "Total Minutes":[],
    "Total Hours": []
    }

locale_list = df['locale'].unique()
for locale in locale_list:
    df_locale = df[df['locale']==locale]
    total_mins = round(float(df_locale['Total Duration - Mins'].sum()),2)
    total_hours = round(float(df_locale['Total Duration - Hours'].sum()),2)
    dict_info['Locale'].append(locale)
    dict_info['Total Minutes'].append(total_mins)
    dict_info['Total Hours'].append(total_hours)

print(dict_info)

df_info = pd.DataFrame(dict_info)
df_info.to_csv(file_path_output, index=False) 

print(df_info)
# print(sum(df['Duration']))

