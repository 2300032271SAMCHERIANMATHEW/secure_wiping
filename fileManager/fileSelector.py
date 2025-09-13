# fileSelector.py
import os

def select_files_in_folder(folder_path):
    """
    Recursively walk through a folder and return all file paths.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"{folder_path} does not exist")

    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_list.append(full_path)
    return file_list


def select_single_file(file_path):
    """
    Select a single file if it exists.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist or is not a file")
    return [file_path]
