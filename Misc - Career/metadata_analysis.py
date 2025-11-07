import pandas as pd
from datetime import time
import glob
import os

path_files = '/Users/joaopedrosantosmartins/Documents/Clients/Voicemod/Metadata - OTS Monologue/*.tsv' # use your path
output_file = "OTS_Monologue_High_Quality_Metadata_Breadkdown.csv"
file_path_output = path_files.replace(path_files.split("/")[-1],output_file)
print(file_path_output)

dict_info = {
    "Dataset Name":[], 
    "Language": [], 
    "Duration per Speaker - Seconds Avg.": [],
    "Total Seconds Available":[],
    "Total Minutes Available":[],
    "Total Hours Available": [], 
    "Total Audio Files":[],
    "Unique Speakers - Count":[],
    "Domain":[],
    "Sample Rates":[]
    }

all_files = glob.glob(path_files)

# TEST
# test_file = '/Users/joaopedrosantosmartins/Documents/Clients/Voicemod/Metadata - OTS Monologue/en-us_OTS-speech-scriptedMonologue_globalaffairs.tsv'
# all_files = [test_file]

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, delimiter='\t')
    
    # Filter Info Based on Sample Rate
    df = df[df['SampleRate']>=44100]
    # print(df.columns.values.tolist())
    # print(df['SampleRate'].unique())
    # print(df['SampleRate'].unique()[0],df['SampleRate'].unique()[-1])
    if len(df['SampleRate'].unique()) == 0:
        pass
    elif df['SampleRate'].unique()[0] >= 44100:
        # print(df['SampleRate'].unique)
        # Extract Info
        lang = filename.split('/')[-1].split('_')[0]
        # lang = df['PrimaryLanguage'].unique()
        # print(lang)
        domain = filename.split('_')[-1].replace('.tsv','')
        dataset_name = filename.split('/')[-1].replace('.tsv','')
        # if lang not in df_info:
        #     df_info[lang] = []
        df['Duration - Seconds'] = pd.DatetimeIndex(df['Duration']).second
        df['Duration - Minutes'] = pd.DatetimeIndex(df['Duration']).minute
        df['Total Duration - Seconds'] = df['Duration - Minutes'].multiply(60) + df['Duration - Seconds']
        df['Total Duration - Minutes'] = df['Duration - Minutes'] + df['Duration - Seconds'].div(60)
        df['Total Duration - Hours'] = df['Duration - Minutes'].div(60) + df['Duration - Seconds'].div(60*60)

        print(df[['Duration','Duration - Seconds','Duration - Minutes','Total Duration - Seconds','Total Duration - Minutes','Total Duration - Hours']])
        time_avg = round(float(df['Total Duration - Seconds'].mean()),5)
        speaker_count = df['SpeakerId'].nunique()
        sample_rates = list(set(df['SampleRate']))
        
        total_secs = round(float(df['Total Duration - Seconds'].sum()),5)
        total_mins = round(float(df['Total Duration - Minutes'].sum()),5)
        total_hours = round(float(df['Total Duration - Hours'].sum()),5)
        # total_hours = round(float(df['Duration - Seconds'].sum()/(60*60)),2)
        # total_hours = round(sum(float(df['Duration - Seconds'].sum()/(60*60)),float(df['Duration - Minutes'].sum()/(60))),2)
        total_files = int(df['RecordingId'].count())
        
        if len(df['SampleRate'].unique()) >1:
            print(f'MULTIPLE BIT RATE: {dataset_name}\t{sample_rates}')

        else:
            sample_rates = sample_rates[0]
            print(f'{dataset_name}\n{lang}\n{time_avg}\n{total_hours}\n{total_files}\n{speaker_count}\n{domain}\n{sample_rates}\n')
        
        #  Add Info to Dataset
        dict_info['Language'].append(lang)
        dict_info['Dataset Name'].append(dataset_name)
        dict_info['Duration per Speaker - Seconds Avg.'].append(time_avg)
        dict_info['Total Seconds Available'].append(total_secs)
        dict_info['Total Minutes Available'].append(total_mins)
        dict_info['Total Hours Available'].append(total_hours)
        dict_info['Total Audio Files'].append(total_files)

        
        dict_info['Unique Speakers - Count'].append(speaker_count)
        dict_info['Domain'].append(domain)
        dict_info['Sample Rates'].append(sample_rates)
        
    else:
        pass


print(f"DONE\nFile Saved to Path: {file_path_output}")
print(dict_info)

df_info = pd.DataFrame(dict_info)
df_info.to_csv(file_path_output, index=False) 

