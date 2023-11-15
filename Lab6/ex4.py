# Write a Python script that counts the number of files with each extension in a given directory. The script should:
# Accept a directory path as a command line argument (using sys.argv).
# Use the os module to list all files in the directory.
# Count the number of files for each extension (e.g., .txt, .py, .jpg) and print out the counts.
# Include error handling for scenarios such as the directory not being found, no read permissions, or the directory being empty.


import os
import sys

# Ex 4)
def count_files_by_extension(directory_path):
    try:
        # Directory exists
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Error: The directory '{directory_path}' does not exist.")

        # Directory is readable
        if not os.access(directory_path, os.R_OK):
            raise PermissionError(f"Error: No read permissions for directory '{directory_path}'.")

        # All files in the directory
        files = os.listdir(directory_path)

        # Is directory empty
        if not files:
            print(f"The directory '{directory_path}' is empty.")
            return

        # Count files by extension
        extension_counts = {}
        for file in files:
            _, extension = os.path.splitext(file)
            extension = extension.lower()
            extension_counts[extension] = extension_counts.get(extension, 0) + 1

        print(f"File counts by extension in '{directory_path}':")
        for extension, count in extension_counts.items():
            print(f"{extension}: {count} file(s)")

    except FileNotFoundError as e:
        print(e)

    except PermissionError as e:
        print(e)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script_name.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        count_files_by_extension(directory_path)