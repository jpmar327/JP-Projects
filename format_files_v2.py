import os
import shutil
# LOOK OUT FOR FILES LIKE .PNG, .JPG, .MOV, .NEF
# ADD DELETE ORIGINAL FILE FUNCTION: VAL = DELETE_ORIG_YN

# ------------- CHANGE INPUTS BELOW ------------- 
files_prefix = 'RW'
month = '6'
year = '2023'
folder_path = r"C:/Users/jpmar/Pictures/DSLR/Redwoods State Park - June 9 2023"
# ------------------------------------------------

def return_files_types(folder_path):
    ''' 
    Input: Folder path
    Outputs: List of unique file types found in folder
    '''
    files_list = []
    for dirfolder in os.listdir(folder_path):
        files_list.extend(os.listdir(fr"{folder_path}/{dirfolder}"))
    return list(set([file_name.split('.')[-1] for file_name in files_list]))

def create_file_types_folders(folder_path,subfolder,files_type_list):
    for file_type in files_type_list:
        new_folder_path = fr"{folder_path}/{subfolder}/{file_type}/"
        os.makedirs(os.path.dirname(new_folder_path), exist_ok=True)


def format_files(folder_path,subfolder,files_prefix,month,year):
    count = 0
    dsc_tracker = ''

    for dirfolder in os.listdir(folder_path):
        if dirfolder == subfolder:
            break
        for dirname in os.listdir(fr"{folder_path}/{dirfolder}"):
            file_name = dirname.split('.')[0]
            filepath = fr"{dirfolder}/{file_name}"
            if dsc_tracker == '' or filepath != dsc_tracker:
                dsc_tracker = fr"{dirfolder}/{file_name}"
                count += 1
            file_type = dirname.split('.')[-1]

            old_path = fr"{folder_path}/{dirfolder}/{dirname}"
            new_path = fr"{folder_path}/{subfolder}/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
            # print(old_path, new_path)
            shutil.copy(old_path,new_path)

subfolder = 'Formatted'
files_type_list = return_files_types(folder_path)
create_file_types_folders(folder_path,subfolder,files_type_list)
format_files(folder_path,subfolder,files_prefix,month,year)