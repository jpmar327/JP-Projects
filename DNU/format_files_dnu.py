import os
import shutil
# LOOK OUT FOR FILES LIKE .PNG, .JPG, .MOV, .NEF
# ADD DELETE ORIGINAL FILE FUNCTION: VAL = DELETE_ORIG_YN
count = 0
files_prefix = 'Redwoods'
month = '6'
year = '2023'
folder_path = r"C:/Users/jpmar/Pictures/DSLR/Redwoods State Park - June 9 2023"

print(os.listdir(folder_path))
test_dir = os.listdir(folder_path)[0]
print(len(os.listdir(fr"{folder_path}/{test_dir}")))
test_dir = os.listdir(folder_path)[1]
print(len(os.listdir(fr"{folder_path}/{test_dir}")))


for dirfolder in os.listdir(folder_path):
    dsc_tracker = ''
    for dirname in os.listdir(fr"{folder_path}/{dirfolder}"):
        if dsc_tracker == '' or  dirname.split('.')[0] != dsc_tracker:
            dsc_tracker = dirname.split('.')[0]
            count += 1
            print(dsc_tracker)
        file_type = dirname.split('.')[-1]
        old_path = fr"{folder_path}/{dirfolder}/{dirname}"
        new_path = fr"{folder_path}/{dirfolder}/{files_prefix}_{month}_{year}_{count}.{file_type}"
        new_path_dir = fr"C:/Users/jpmar/Pictures/DSLR/Test/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
print(count)
