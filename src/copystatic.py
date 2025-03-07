import os
import shutil


def copy_static_to_public(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.makedirs(destination, exist_ok=True)

    if os.path.exists(source):
        for file in os.listdir(source):
            file_path_source = os.path.join(source, file)
            file_path_destination = os.path.join(destination, file)

            if os.path.isfile(file_path_source):
                shutil.copy(file_path_source, file_path_destination)
            else:
                copy_static_to_public(file_path_source, file_path_destination)
                