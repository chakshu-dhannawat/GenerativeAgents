import os

folder_path = "Assets\\Farewell"  # Specify the path to the folder here

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Sort the files to ensure consistent ordering
files.sort()

# Rename the files
for index, file_name in enumerate(files):
    if file_name.endswith(".png"):
        new_name = f"{index}.png"
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
