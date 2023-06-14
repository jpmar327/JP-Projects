import os
import shutil
# LOOK OUT FOR FILES LIKE .PNG, .JPG, .MOV, .NEF
# count = 0

# ------------- CHANGE INPUTS BELOW ------------- 
files_prefix = 'RW'
month = '6'
year = '2023'
folder_path = r"C:/Users/jpmar/Pictures/DSLR/Redwoods State Park - June 9 2023"
# ------------------------------------------------

# folder_path = r"C:/Users/jpmar/Pictures/DSLR/Test_Pics"
subfolder = 'Formatted'
# output_folder = fr"{folder_path}/Formatted"

# dsc_list = []
# dsc_folder_tracker = ''
# dsc_tracker = ''

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


# def copy_rename_file_to_new_dir(old_path, copy_path, new_path):
#     print(old_path, copy_path, new_path)
#     shutil.copy(old_path,copy_path)
    # os.rename(copy_path, new_path)

# def assign_file_name(folder_path):
#     count = 0
#     dsc_tracker = ''

#     for dirfolder in os.listdir(folder_path):
#         for dirname in os.listdir(fr"{folder_path}/{dirfolder}"):
#             file_name = dirname.split('.')[0]
#             filepath = fr"{dirfolder}/{file_name}"
#             if dsc_tracker == '' or filepath != dsc_tracker:
#                 dsc_tracker = fr"{dirfolder}/{file_name}"
#                 count += 1
#             file_type = dirname.split('.')[-1]

def format_files(folder_path,subfolder,files_prefix,month,year):
    count = 0
    dsc_tracker = ''
    files_type_list = return_files_types(folder_path)
    create_file_types_folders(folder_path,subfolder,files_type_list)

    for dirfolder in os.listdir(folder_path):
        # if dirfolder == 'Formatted':
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
            # copy_path = fr"{folder_path}/{subfolder}/{file_type}/{dirname}"
            new_path = fr"{folder_path}/{subfolder}/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
            # copy_rename_file_to_new_dir(old_path, copy_path, new_path)
            # print(old_path, copy_path, new_path)
            print(old_path, new_path)
            shutil.copy(old_path,new_path)
            # os.rename(copy_path, new_path)
# #         new_path_dir = fr"C:/Users/jpmar/Pictures/DSLR/Test/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
# #         # # if dirname.split('.')[0] != dsc_tracker:
# #         # #    dsc_tracker 
# #         # # print(count,dsc_tracker,file_type,dirname)
# #         # shutil.move(old_path, new_path_dir)

# #         # # os.rename(old_path, new_path)
# #         # # print(old_path, new_path)
        
# #         # shutil.move(new_path, new_path_dir)
        
# #         # print(fr"/{dirfolder}/{dirname}", fr'/{dirfolder}/{files_prefix}_{month}_{year}_{count}.{file_type}', fr"/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}")
# #         # print(f"{dirfolder.split('D3100')[0]}_{dirname} -- {files_prefix}_{month}_{year}_{count}.{file_type}")
# #         # print(f"{dirname} -- {files_prefix}_{month}_{year}_{count}.{file_type}")
# #     # if os.path.isdir(dirname):
# #     #     for i, filename in enumerate(os.listdir(dirname)):
# #     #         print(dirname)
# #             # os.rename(dirname + "/" + filename, dirname + "/" + str(i) + ".bmp")
# # print(count)

# # # for dirfolder in os.listdir(folder_path):
# # #     dsc_tracker = ''
# # #     for dirname in os.listdir(fr"{folder_path}/{dirfolder}"):
# # #         if dsc_tracker == '' or  dirname.split('.')[0] != dsc_tracker:

format_files(folder_path,subfolder,files_prefix,month,year)