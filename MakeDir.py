import os

path_to_base_folder = r"""J:\Petru\Projects\Results\Vid4\Hands\Movement"""
folder_name_suffix = "move"
num_of_folders = 500
starting_index = 250

def make_folders(number_of_folders):
    os.chdir(path_to_base_folder)
    for i in range(number_of_folders):
        os.mkdir(folder_name_suffix+str(i+starting_index))

make_folders(num_of_folders)
