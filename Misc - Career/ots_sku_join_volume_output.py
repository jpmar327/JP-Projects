import pandas as pd
from datetime import time
import glob
import os

# MERGING ALL METADATA
# path_files = '/Users/joaopedrosantosmartins/Documents/Clients/Voicemod/Metadata - OTS Monologue/*.tsv' # use your path
path_folder = '/Users/joaopedrosantosmartins/Documents/Clients/Genesys/Metadata/07.23.2025 - OTS H2H Metadata - Multi-lingual/*'
file_path_output = '/Users/joaopedrosantosmartins/Documents/Clients/Genesys/Metadata/07.23.2025 - OTS H2H Metadata - Multi-lingual/Merged Metadata.csv'
file_client_request = '/Users/joaopedrosantosmartins/Documents/Clients/Genesys/Requests/recordings_multi-ling_selection_20250723-a.csv'
path_folders = glob.glob(path_folder)
# output_file = "OTS_Monologue_High_Quality_Metadata_Breadkdown.csv"
# file_path_output = path_files.replace(path_files.split("/")[-1],output_file)
# print(file_path_output)
files_list = []
if file_path_output not in glob.glob('/Users/joaopedrosantosmartins/Documents/Clients/Genesys/Metadata/07.23.2025 - OTS H2H Metadata - Multi-lingual/*.csv'):
    print('\nCONSOLIDATING ALL METADATA\n')
    for metadata_folder in path_folders:
        print(metadata_folder)
        file_path = glob.glob(f'{metadata_folder}/*.tsv')
        print(file_path)
        files_list.extend(file_path)

    print(files_list)
    df_list = []
    for filename in files_list:
        df = pd.read_csv(filename, index_col=None, delimiter='\t')
        df_list.append(df)

    df_all = pd.concat(df_list, axis=0, ignore_index=True)
    # print(df_all)
    df_all.to_csv(file_path_output, index=False)
else:
    print('METADATA ALREADY JOINED. OPENING FILE.')
    df_all = pd.read_csv(file_path_output)

print(df_all.columns.values.tolist())


# JOINING METADATA W/ CLIENT REQUEST
df_request = pd.read_csv(file_client_request, index_col=None, delimiter='\t')
print(df_request.columns.values.tolist())
df_joined = pd.merge(df_request, df_all, on=["RecordingId"], how="left")
print(df_joined)
df_joined.to_csv(file_path_output.replace('Merged Metadata','Metadata Requested From Client'), index=False)

# dict_info = {
#     "Dataset Name":[], 
#     "Language": [], 
#     "Duration per Speaker - Seconds Avg.": [], 
#     "Total Hours Available": [], 
#     "Total Audio Files":[],
#     "Unique Speakers - Count":[],
#     "Domain":[],
#     "Sample Rates":[]
#     }

# all_files = glob.glob(path_files)
# print(all_files)