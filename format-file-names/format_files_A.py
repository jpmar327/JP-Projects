import os
import shutil
# LOOK OUT FOR FILES LIKE .PNG, .JPG, .MOV, .NEF
# ADD DELETE ORIGINAL FILE FUNCTION: VAL = DELETE_ORIG_YN

# ------------- CHANGE INPUTS BELOW ------------- 
files_prefix = 'JP_Film'
month = '2'
year = '2026'
folder_path = r"C:\Users\jpmar\Pictures\Film\Test"
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


def format_files(folder_path,subfolder,files_prefix,month,year,files_type_list):
    for file_type_check in files_type_list:
        count = 0
        dsc_tracker = ''
        for dirfolder in os.listdir(folder_path):
            # print(dirfolder)
            if dirfolder == subfolder:
                break
            for dirname in os.listdir(fr"{folder_path}/{dirfolder}"):
                file_type = dirname.split('.')[-1]
                if file_type_check.lower() == file_type.lower():
                    print(dirname)
                    file_name = dirname.split('.')[0]
                    filepath = fr"{dirfolder}/{file_name}"
                    if dsc_tracker == '' or filepath != dsc_tracker:
                        dsc_tracker = fr"{dirfolder}/{file_name}"
                        count += 1
                        file_name_0_limit = 5
                        file_count_str = int(file_name_0_limit-len(str(count)))*"0"+str(count)
                    

                    
                    print(file_type)
                    old_path = fr"{folder_path}/{dirfolder}/{dirname}"
                    new_path = fr"{folder_path}/{subfolder}/{file_type}/{files_prefix}_{month}_{year}_{file_count_str}.{file_type}"
                    print(new_path)
                    # print(old_path, new_path)
                    shutil.copy(old_path,new_path)

def main():
    subfolder = 'Formatted'
    print(f'\nFORMATTING PHOTOS\nFOLDER PATH INPUT: "{folder_path}"\n')
    files_type_list = return_files_types(folder_path)
    print(files_type_list)
    create_file_types_folders(folder_path,subfolder,files_type_list)
    format_files(folder_path,subfolder,files_prefix,month,year,files_type_list)
    print(f'DONE FORMATTING PHOTOS\nFOLDER PATH OUTPUT: "{folder_path}/{subfolder}"\n')

if __name__ == "__main__":
    main()