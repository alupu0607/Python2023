# Write a script using the os module that renames all files in a specified directory to have a
# sequential number prefix. For example, file1.txt, file2.txt, etc. 
# Include error handling for cases like the directory not existing or files
# that can't be renamed.


import os
import sys


def rename_files_with_prefix(directory_path):
    try:
        if not os.path.isdir(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        files = os.listdir(directory_path)

        if not files:
            print(f"No files found in the directory: {directory_path}")
            return

        counter = 1
        for filename in sorted(files):
            old_path = os.path.join(directory_path, filename)
            new_filename = f"file{counter}.{filename.split('.')[-1]}"
            new_path = os.path.join(directory_path, new_filename)

            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                counter += 1
            except PermissionError as e:
                print(f"Error renaming {filename}: Permission denied. {e}")
            except Exception as e:
                print(f"Error renaming {filename}: {e}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Lab6/ex1.py  <directory_path>")
    else:
        rename_files_with_prefix(sys.argv[1])

# python Lab6/ex2.py D:\University\Example