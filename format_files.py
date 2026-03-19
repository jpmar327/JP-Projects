import os
import shutil
# LOOK OUT FOR FILES LIKE .PNG, .JPG, .MOV, .NEF
# ADD DELETE ORIGINAL FILE FUNCTION: VAL = DELETE_ORIG_YN

'''----------------------------- CHANGE INPUTS BELOW -----------------------------'''
files_prefix = 'MF'
month = '9'
year = '2024'
# main_folder_path = r"C:/Users/jpmar/Pictures/DSLR/Redwoods State Park - June 9 2023"
main_folder_path = r"C:\Users\jpmar\Documents\Pictures\DSLR\Mateus 1st Birthday - September 2024"

'''----------------------------- FUNCTIONS -----------------------------'''

def lookup_files(path):
    files_path_list = {}
    check_file_types = (".JPG", ".PNG", ".NEFF",".GIF")
    for root, dirs, files in os.walk(path):
        if len([f for f in files if f.upper().endswith(check_file_types)]) > 0:
            files_path_list[root] = files
    return files_path_list

def prep_directory_for_copy(main_folder_path, copy_path_list):
    files_type_list = list(set([file_name.split('.')[-1].upper() for file_name in copy_path_list]))
    # print(files_type_list)
    for file_type in files_type_list:
        new_folder_path = os.path.join(main_folder_path, file_type)
        os.makedirs(new_folder_path, exist_ok=True)

def prep_file_paths(files_path_list):
    file_type_count_tracker = {}
    files_path_dict = {}
    for key, value in files_path_list.items():
        # print('testw',key,value)
        for file in value:
            file_type = file.split('.')[-1]
            if file_type not in file_type_count_tracker.keys():
                file_type_count_tracker[file_type] = 1
            else:
                file_type_count_tracker[file_type] += 1
            filepath = os.path.join(key, file)
            count = file_type_count_tracker[file_type]
            new_path = os.path.join(main_folder_path, file_type.upper(), fr"{files_prefix}_{month}_{year}_{count}.{file_type}")
            files_path_dict[filepath] = new_path
    return files_path_dict


def copy_file_to_new_path(copy_path_dict):
    for copy_path in copy_path_dict:
        print('------------------------------------------------------')
        print(copy_path)
        print(copy_path_dict[copy_path])
        shutil.copy(copy_path,copy_path_dict[copy_path])

'''----------------------------- MAIN FUNCTION -----------------------------'''

def main():
    print(f'\nFORMATTING PHOTOS\nFOLDER PATH INPUT: "{main_folder_path}"\n')
    files_path_list = lookup_files(os.path.join(main_folder_path))
    copy_path_dict = prep_file_paths(files_path_list)
    prep_directory_for_copy(main_folder_path, list(copy_path_dict.values()))
    copy_file_to_new_path(copy_path_dict)
    print(f'DONE FORMATTING PHOTOS\nFOLDER PATH OUTPUT: "{main_folder_path}"\n')

if __name__ == "__main__":
    main()


'''----------------------------- DNU BELOW BUT CAN BE USEFUL -----------------------------'''

def check_if_file(file_path):
    return os.path.isfile(file_path)

def return_files_types(main_folder_path):
    ''' 
    Input: Folder path
    Outputs: List of unique file types found in folder
    '''
    print("\nFUNCTION: return_file_types(main_folder_path)")
    files_list = []
    for dirfolder in os.listdir(main_folder_path):
        # files_dir = os.path.join(main_folder_path,dirfolder)
        
        files_list.extend(os.listdir(os.path.join(main_folder_path, dirfolder)))

    file_types_list = list(set([file_name.split('.')[-1] for file_name in files_list]))
    print(file_types_list)
    print("FUNCTION END\n")
    return file_types_list

def create_file_types_folders(main_folder_path,subfolder,files_type_list):
    print("\nFUNCTION: create_file_types_folders(main_folder_path,subfolder,files_type_list):")
    for file_type in files_type_list:
        new_folder_path = os.path.join(main_folder_path, subfolder, file_type)
        # print(os.path.dirname(new_folder_path))
        print(new_folder_path)
        # os.makedirs(os.path.dirname(new_folder_path), exist_ok=True)
        os.makedirs(new_folder_path, exist_ok=True)
        print("FUNCTION END\n")