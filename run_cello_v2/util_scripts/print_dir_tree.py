import os

def print_tree(starting_dir):
    for dirpath, dirnames, filenames in os.walk(starting_dir):
        print(f"Directory: {dirpath}")
        for dirname in dirnames:
            print(f"\tSubdirectory: {os.path.join(dirpath, dirname)}")

dir = "/Users/jiweiqi/Work/Cello/"

additional_path= input("you can specify a specific folder or path within Cello: ")

if len(additional_path) > 0:
    print_tree(dir + additional_path)
else:
    print_tree(dir)
