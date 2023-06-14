import os
import shutil
# LOOK OUT FOR FILES LIKE .PNG, .JPG, .MOV, .NEF
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
    # print(dirfolder)
    dsc_tracker = ''
    for dirname in os.listdir(fr"{folder_path}/{dirfolder}"):
        # print(dirname)
        if dsc_tracker == '' or  dirname.split('.')[0] != dsc_tracker:
            dsc_tracker = dirname.split('.')[0]
            count += 1
            print(dsc_tracker)
        file_type = dirname.split('.')[-1]
        # if file_type == 'JPG':
        #     print(file_type)
        old_path = fr"{folder_path}/{dirfolder}/{dirname}"
        new_path = fr"{folder_path}/{dirfolder}/{files_prefix}_{month}_{year}_{count}.{file_type}"
        new_path_dir = fr"C:/Users/jpmar/Pictures/DSLR/Test/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}"
        # # if dirname.split('.')[0] != dsc_tracker:
        # #    dsc_tracker 
        # # print(count,dsc_tracker,file_type,dirname)
        # shutil.move(old_path, new_path_dir)
        # # os.rename(old_path, new_path)
        # # print(old_path, new_path)
        
        # shutil.move(new_path, new_path_dir)
        
        # print(fr"/{dirfolder}/{dirname}", fr'/{dirfolder}/{files_prefix}_{month}_{year}_{count}.{file_type}', fr"/{file_type}/{files_prefix}_{month}_{year}_{count}.{file_type}")
        # print(f"{dirfolder.split('D3100')[0]}_{dirname} -- {files_prefix}_{month}_{year}_{count}.{file_type}")
        # print(f"{dirname} -- {files_prefix}_{month}_{year}_{count}.{file_type}")
    # if os.path.isdir(dirname):
    #     for i, filename in enumerate(os.listdir(dirname)):
    #         print(dirname)
            # os.rename(dirname + "/" + filename, dirname + "/" + str(i) + ".bmp")
print(count)

# for dirfolder in os.listdir(folder_path):
#     dsc_tracker = ''
#     for dirname in os.listdir(fr"{folder_path}/{dirfolder}"):
#         if dsc_tracker == '' or  dirname.split('.')[0] != dsc_tracker: