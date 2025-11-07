import pandas as pd
from datetime import time
import glob
import os


'''--------------------------------- INPUTS SECTION ---------------------------------'''

metadata_folder_path = rf'[FILE PATH]\*.tsv'

file_path_output = rf'[FILE PATH]\Metadata_Breakdown.csv'
file_path_token_count_output = rf'[FILE PATH]\Average Transcript Tokens per Recording.csv'


dict_info = {
    "Dataset Name":[], 
    "Language": [], 
    "Time Duration - Seconds Avg.": [],
    "Time Duration - Minutes Avg.":[],
    "Time Duration - Hours Avg.":[],
    "Unique Conversations - Count":[],
    }

dict_token = {
    "Dataset Name":[], 
    "Average Token Count": []
}

# fields_count = ['RecordingId']
recording_id_field = 'RecordingId'
transcript_field = 'Transcription'
relative_file_name_field = 'RelativeFileName'

'''--------------------------------- DEF MAIN SECTION ---------------------------------'''
def main_analyze_data():
    # dict_info = {}
    files_list = output_files_list(metadata_folder_path)
    for filename in files_list:
        df = read_metadata(filename)
        df = add_dataset_name(df, filename)
        df = add_locale(df, filename)
        # print(df.columns.values.tolist())
        # for field in fields_count:
        #     field_count = count_unique_values(df,field)
        unique_convo_count = count_unique_values(df,recording_id_field)
        df, time_avg_secs = average_time_duration_secs(df)
        df, time_avg_mins = average_time_duration_mins(df)
        df, time_avg_hrs = average_time_duration_hrs(df)
        dataset_name = extract_dataset_name(df)
        locale = extract_locale(df)
        # print(field_count,time_avg_secs,time_avg_mins,time_avg_hrs)
        dict_info['Dataset Name'].append(dataset_name)
        dict_info['Language'].append(locale)
        dict_info["Unique Conversations - Count"].append(unique_convo_count)
        dict_info['Time Duration - Seconds Avg.'].append(time_avg_secs)
        dict_info['Time Duration - Minutes Avg.'].append(time_avg_mins)
        dict_info['Time Duration - Hours Avg.'].append(time_avg_hrs)
    print(dict_info)
    df_info = pd.DataFrame(dict_info)
    print(df_info)
    df_info.to_csv(file_path_output, index=False)

def main_transcript_token_average():
    dict_token = {
        "Dataset Name":[], 
        "Average Token Count": []
    }
    files_list = output_files_list(metadata_folder_path)
    for filename in files_list:
        df = read_metadata(filename)
        df = add_dataset_name(df, filename)
        dict_token['Dataset Name'].append(extract_dataset_name(df))
        dict_token['Average Token Count'].append(transcript_token_count(df,transcript_field,relative_file_name_field))
        # df, token_count_avg = transcript_token_count(df,transcript_field,relative_file_name_field)
        # df['token_count'] = df[transcript_field].apply(lambda x: len(x.split()))
        # print(token_count_avg)
    print(dict_token)
    df_token = pd.DataFrame(dict_token)
    print(df_token)
    df_token.to_csv(file_path_token_count_output, index=False)

'''--------------------------------- DEF METADATA ANALYSIS FUNTIONS ---------------------------------'''

def output_files_list(folder_path):
    return glob.glob(folder_path)

def read_metadata(metadata_path):
    if ".tsv" in metadata_path:
        df = pd.read_csv(metadata_path, index_col=None, delimiter='\t')
    else:
        df = pd.read_csv(metadata_path, index_col=None)
    return df

def add_dataset_name(df, filename):
    if "/" in filename:
        dataset_name = filename.split("/")[-1].replace('.tsv',"").replace(".csv","")
    else:
        dataset_name = filename.split("\\")[-1].replace('.tsv',"").replace(".csv","")
    df['dataset_name'] = dataset_name
    return df

def add_locale(df, filename):
    if "/" in filename:
        locale = filename.split("/")[-1].split('_')[0]
    else:
        locale = filename.split("\\")[-1].split('_')[0]
    df['locale'] = locale
    return df

def format_time_duration(df):
    df['Duration - Seconds'] = pd.DatetimeIndex(df['Duration']).second
    df['Duration - Minutes'] = pd.DatetimeIndex(df['Duration']).minute
    df['Total Duration - Seconds'] = df['Duration - Minutes'].multiply(60) + df['Duration - Seconds']
    df['Total Duration - Minutes'] = df['Duration - Minutes'] + df['Duration - Seconds'].div(60)
    df['Total Duration - Hours'] = df['Duration - Minutes'].div(60) + df['Duration - Seconds'].div(60*60)
    return df

def extract_locale(df):
    return df['locale'].iloc[0]

def extract_dataset_name(df):
    return df['dataset_name'].iloc[0]

def count_unique_values(df,field):
    field_count = int(df[field].nunique())
    return field_count

def average_time_duration_secs(df):
    if 'Total Duration - Seconds' not in df.columns.values.tolist():
        df = format_time_duration(df)
    time_avg = round(float(df['Total Duration - Seconds'].mean()),5)
    return df, time_avg

def average_time_duration_mins(df):
    if 'Total Duration - Minutes' not in df.columns.values.tolist():
        df = format_time_duration(df)
    time_avg = round(float(df['Total Duration - Minutes'].mean()),5)
    return df, time_avg

def average_time_duration_hrs(df):
    if 'Total Duration - Hours' not in df.columns.values.tolist():
        df = format_time_duration(df)
    time_avg = round(float(df['Total Duration - Hours'].mean()),5)
    return df, time_avg

def transcript_token_count(df,token_field,group_field):
    df = df.drop_duplicates(subset=[token_field])
    print(df[token_field])
    df['token_count'] = df[token_field].apply(lambda x: len(x.split()))
    df = df.groupby([group_field], as_index=False)['token_count'].sum()
    df.to_csv(file_path_token_count_output, index=False)
    token_count_avg = round(float(df['token_count'].mean()),5)
    # return df, token_count_avg
    return token_count_avg
'''--------------------------------- FUNCTION MAIN() TRIGGER ---------------------------------'''
if __name__ == '__main__':
    main_analyze_data()
    # main_transcript_token_average()