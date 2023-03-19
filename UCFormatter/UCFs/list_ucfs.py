'''
If you run this file, it will try to:

1. retrieve ucfs from your local folder
2. save them onto this current folder
3. save all of the files to ucf-list.txt

You can modify it to do something else

By default, it doesn't need to be run,
UNLESS you have a new/modified BASE UCF
to add
'''

import os
import shutil
import glob


local_ucf_dir = '../../../IO/inputs'

# UCFs_dir : a folder named 'UCFs' in this repo
# default, this is that folder
def list_ucfs_txt(UCFs_dir='.'):
    cur_dir = os.getcwd()
    os.chdir(UCFs_dir)
    extensions = ['.input.json', '.output.json', '.UCF.json']
    ucf_list = []
    for e in extensions:
        ucf_files = list(glob.glob('*' + e))
        ucf_list += ucf_files
    ucf_list = sorted(ucf_list)
    with open('ucf-list.txt', 'w') as f:
        f.write("\n".join(ucf_list))
    os.chdir(cur_dir)

# local_dir : path to folder where you have UCFs on your computer
def retrieve_local_ucfs(local_dir, repo_dir='.'):
    cur_dir = os.getcwd()
    os.chdir(local_dir)
    extension = '.json'
    ucf_files = sorted(list(glob.glob('*' + extension)))
    os.chdir(cur_dir)
    for filename in ucf_files:
        source_path = os.path.join(local_dir, filename)
        dest_path = os.path.join(repo_dir, filename)
        shutil.copy(source_path, dest_path)
        
if __name__ == '__main__':
    retrieve_local_ucfs(local_ucf_dir)
    ucf_list = list_ucfs_txt()
    print("O.K!")
