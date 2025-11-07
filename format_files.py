import os
import shutil
# LOOK OUT FOR FILES LIKE .PNG, .JPG, .MOV, .NEF
# ADD DELETE ORIGINAL FILE FUNCTION: VAL = DELETE_ORIG_YN

# ------------- CHANGE INPUTS BELOW ------------- 
files_prefix = 'MF'
month = '10'
year = '2024'
# folder_path = r"C:/Users/jpmar/Pictures/DSLR/Redwoods State Park - June 9 2023"
folder_path = r"C:\Users\jpmar\Documents\Pictures\DSLR\test"
# ------------------------------------------------

def return_files_types(folder_path):
    ''' 
    Input: Folder path
    Outputs: List of unique file types found in folder
    '''
    print("\nFUNCTION: return_file_types(folder_path)")
    files_list = []
    for dirfolder in os.listdir(folder_path):
        # files_dir = os.path.join(folder_path,dirfolder)
        
        files_list.extend(os.listdir(os.path.join(folder_path, dirfolder)))
        # print(files_list)
        # print(dirfolder)
        # print(files_dir)

    file_types_list = list(set([file_name.split('.')[-1] for file_name in files_list]))
    print(file_types_list)
    print("FUNCTION END\n")
    return file_types_list

def create_file_types_folders(folder_path,subfolder,files_type_list):
    print("\nFUNCTION: create_file_types_folders(folder_path,subfolder,files_type_list):")
    for file_type in files_type_list:
        new_folder_path = os.path.join(folder_path, subfolder, file_type)
        # print(os.path.dirname(new_folder_path))
        print(new_folder_path)
        # os.makedirs(os.path.dirname(new_folder_path), exist_ok=True)
        os.makedirs(new_folder_path, exist_ok=True)
        print("FUNCTION END\n")


def lookup_files(path):
    # test_count = 0
    files_path_list = {}
    check_file_types = (".JPG", ".PNG", ".NEFF",".GIF")
    for root, dirs, files in os.walk(path):
        if len([f for f in files if f.upper().endswith(check_file_types)]) > 0:
            files_path_list[root] = files
            # print([f for f in files if f.endswith((".JPG", ".PNG"))])
    # print('test',files_path_list)
        # for file in files:
        #     print(file)
    return files_path_list
        # if len(files) > 0:
        #     test_count +=1
        #     files_path_list[root] = files
        #     print(test_count,root,files,dirs)
        #     print(files_path_list)
        # for check in check_file_types:
        #     print(check,files)
        #     print(check in files)
        #     if check in files:
        #         test_count +=1
        #         files_path_list[root] = files
        #         print(test_count,root,files,dirs)
        #         print(files_path_list)
        #     else:
        #         # print(test_count,root,files,dirs)
        #         pass
        # for name in files:
        #     if name.endswith((".JPG", ".PNG")):
        #         test_count +=1
        #         files_path_list[root] = files
        #         # print(test_count,root,files,dirs)
        #         print(files_path_list)

def prep_file_paths(files_path_list):
    # filepath = os.path.join(folder_path, dirfolder, dirname)
    # count = 0
    # dsc_tracker = ''
    file_type_count_tracker = {}
    files_path_dict = {}
    for key, value in files_path_list.items():
        # print('testw',key,value)
        for file in value:
            file_type = file.split('.')[-1]
            if file_type not in file_type_count_tracker.keys():
                file_type_count_tracker[file_type] = 0
            else:
                file_type_count_tracker[file_type] += 1
            filepath = os.path.join(key, file)
            count = file_type_count_tracker[file_type]
            new_path = os.path.join(folder_path, file_type.upper(), fr"{files_prefix}_{month}_{year}_{count}.{file_type}")
            # old_path_list.append(filepath)
            # files_path_dict[filepath] = os.path.join(folder_path, file)
            files_path_dict[filepath] = new_path
    return files_path_dict


    #     # if check_if_file(filepath):
    #     #     prep_file_paths()
    #     if dsc_tracker == '' or filepath != dsc_tracker:
    #         dsc_tracker = os.path.join(folder_path, dirfolder, dirname)
    #         count += 1
    #     file_type = dirname.split('.')[-1]
    # print(files_path_dict)

        # # # old_path = fr"{folder_path}/{dirfolder}/{dirname}"
        # # print(fr"{folder_path}/{dirfolder}/")
        # old_path = os.path.join(folder_path, dirfolder,dirname)
        # # # new_path = fr"{folder_path}/{subfolder}/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
        # new_path = os.path.join(folder_path, subfolder, file_type, fr"{files_prefix}_{month}_{year}_{count}.{file_type}")
        # copy_path_dict[old_path] = new_path


    # for files in files_path_list:
    #     folder_path = files_path_list
    # if dsc_tracker == '' or filepath != dsc_tracker:
    #     dsc_tracker = os.path.join(folder_path, dirfolder, dirname)
    #     count += 1
    # file_type = dirname.split('.')[-1]
    # # # old_path = fr"{folder_path}/{dirfolder}/{dirname}"
    # # print(fr"{folder_path}/{dirfolder}/")
    # old_path = os.path.join(folder_path, dirfolder,dirname)
    # # # new_path = fr"{folder_path}/{subfolder}/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
    # new_path = os.path.join(folder_path, subfolder, file_type, fr"{files_prefix}_{month}_{year}_{count}.{file_type}")
    # copy_path_dict[old_path] = new_path



def prep_files_for_transfer(folder_path,subfolder,files_prefix,month,year):
    count = 0
    dsc_tracker = ''
    # copy_path_dict = {}
    # lookup_files(os.path.join(folder_path))
    # print(os.listdir(folder_path))
    files_path_list = lookup_files(os.path.join(folder_path))
    # print(files_path_list)
    files_path_dict = prep_file_paths(files_path_list)
    print(files_path_dict)
    for key, value in files_path_dict.items():
        # print(key)
        print(f'{key}\n{value}\n')


    for dirfolder in os.listdir(folder_path):
        if dirfolder == subfolder:
            print('FORMATTED')
            break
        # for dirname in os.listdir(os.path.join(folder_path,dirfolder)):
        #     files_path_list = lookup_files(os.path.join(folder_path,dirfolder,dirname))
        #     print(files_path_list)
        #     prep_file_paths(files_path_list)
            # print(os.listdir(os.path.join(folder_path,dirfolder)))
            # print(os.listdir(fr"{folder_path}\{dirfolder}"))
            # print(f"PATH NAME: {os.path.join(folder_path, dirfolder,dirsubfolder)}")
            # print(os.listdir(os.path.join(folder_path, dirfolder)))
            # print(dirname)
            # print(os.path.join(folder_path,dirfolder))
            # print("list",os.listdir(os.path.join(folder_path,dirfolder)))
            # for dirname in os.listdir(os.path.join(folder_path,dirfolder)):
            # file_name = dirname.split('.')[0]
            # print(f"FILE NAME: {file_name}")
            
            # # filepath = fr"{dirfolder}\{file_name}"
            # filepath = os.path.join(folder_path, dirfolder, dirname)
            # # if check_if_file(filepath):
            # #     prep_file_paths()
            # if dsc_tracker == '' or filepath != dsc_tracker:
            #     dsc_tracker = os.path.join(folder_path, dirfolder, dirname)
            #     count += 1
            # file_type = dirname.split('.')[-1]


            # # # old_path = fr"{folder_path}/{dirfolder}/{dirname}"
            # # print(fr"{folder_path}/{dirfolder}/")
            # old_path = os.path.join(folder_path, dirfolder,dirname)
            # # # new_path = fr"{folder_path}/{subfolder}/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
            # new_path = os.path.join(folder_path, subfolder, file_type, fr"{files_prefix}_{month}_{year}_{count}.{file_type}")
            # copy_path_dict[old_path] = new_path
            
            # print(copy_path_dict)
            # print(f"OLD PATH: {old_path}")dirname
            # print(f"NEW PATH: {new_path}")
        #     print(old_path, new_path)
        #     shutil.copy(old_path,new_path)
    # print(copy_path_dict)
    # return copy_path_dict

def copy_file_to_new_path(copy_path_dict):
    for copy_path in copy_path_dict:
        print('---------------------------------------------')
        print(copy_path)
        print(copy_path_dict[copy_path])
        shutil.copy(copy_path,copy_path_dict[copy_path])

def check_if_file(file_path):
    return os.path.isfile(file_path)



def main():
    # subfolder = 'Formatted'
    print(f'\nFORMATTING PHOTOS\nFOLDER PATH INPUT: "{folder_path}"\n')
    # files_type_list = return_files_types(folder_path)
    # copy_path_dict = prep_files_for_transfer(folder_path,subfolder,files_prefix,month,year)
    files_path_list = lookup_files(os.path.join(folder_path))
    print(files_path_list.values())
    copy_path_dict = prep_file_paths(files_path_list)
    # create_file_types_folders(folder_path,subfolder,files_type_list)
    copy_file_to_new_path(copy_path_dict)
    print(f'DONE FORMATTING PHOTOS\nFOLDER PATH OUTPUT: "{folder_path}"\n')

if __name__ == "__main__":
    main()