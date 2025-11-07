import pandas as pd
from datetime import time
import glob
import os

'''--------------------------------- INPUTS SECTION---------------------------------'''

path_folder = rf'[FILE PATH]\*.tsv'

file_path_output = rf'[FILE PATH]\Merged Metadata.csv'


'''--------------------------------- DEF MAIN SECTION---------------------------------'''
def main():
    read_merge_tsv(path_folder,file_path_output)

'''--------------------------------- TSV MERGE SECTION---------------------------------'''
def read_merge_tsv(path_folder,file_path_output):
    path_folders = glob.glob(path_folder)
    files_list = []
    if file_path_output not in glob.glob(file_path_output):

        print('\nCONSOLIDATING ALL METADATA\n')
        for metadata_folder in path_folders:
            print(metadata_folder)

            files_list.append(metadata_folder)

            print(files_list)
        df_list = []
        for filename in files_list:
            df = pd.read_csv(filename, index_col=None, delimiter='\t')
            if "/" in filename:
                dataset_name = filename.split("/")[-1].replace('.tsv',"").replace(".csv","")
            else:
                dataset_name = filename.split("\\")[-1].replace('.tsv',"").replace(".csv","")
            print(dataset_name)
            df['dataset_name'] = dataset_name
            df_list.append(df)

        df_all = pd.concat(df_list, axis=0, ignore_index=True)
        # print(df_all)
        df_all.to_csv(file_path_output, index=False)
    else:
        print('METADATA ALREADY JOINED. OPENING FILE.')
        df_all = pd.read_csv(file_path_output)

    print(df_all.columns.values.tolist())

'''--------------------------------- FUNCTION MAIN() TRIGGER ---------------------------------'''

if __name__ == '__main__':
    main()