import os
import shutil
import os
from os import listdir

import utils.constants as util

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


origin_dir_list = [util.DATASETFOLDER + '/' + f for f in listdir(util.DATASETFOLDER)]

dir_list = [os.path.basename(f) for f in listdir(util.DATASETFOLDER)]

indexe = 0
files_lens = len(dir_list)
while indexe < files_lens:
    path, ext = os.path.splitext(dir_list[indexe])
    path, ext = os.path.splitext(origin_dir_list[indexe])
    if ext == '.json':
        del dir_list[indexe]
        del origin_dir_list[indexe]
        files_lens = files_lens - 1
        continue
    indexe = indexe + 1

print(dir_list)
print(origin_dir_list)
copy_dir_list = [f'C:/Users/alsgu/OneDrive/바탕 화면/result/{f}' for f in listdir('C:/Users/alsgu/OneDrive/바탕 화면/result')]
print(copy_dir_list)

length = len(origin_dir_list)
for i in range(length):
    shutil.copy(f'{origin_dir_list[i]}/execute_result.json',f'{copy_dir_list[i]}/execute_result.json')
    shutil.copy(f'{origin_dir_list[i]}/intro_info.json',f'{copy_dir_list[i]}/intro_info.json')