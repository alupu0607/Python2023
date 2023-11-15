# Create a Python script that does the following:
# Takes a directory path and a file extension as command line arguments (use sys.argv).
# Searches for all files with the given extension in the specified directory (use os module).
# For each file found, read its contents and print them.
# Implement exception handling for invalid directory paths, incorrect file extensions, and file access errors.
import os
import sys

def read_files_in_directory(directory_path, file_extension):
    try:
        if not os.path.isdir(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        # Validate file extension
        if not file_extension.startswith('.'):
            raise ValueError("Invalid file extension. It should start with a dot (.)")

        found_files = False
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            _, current_extension = os.path.splitext(filename)
            
            if os.path.isfile(file_path) and current_extension == file_extension:
                try:
                    with open(file_path, 'r') as file:
                        file_contents = file.read()
                        print(f"Contents of {filename}:\n{file_contents}\n")
                        found_files = True
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                    
        if not found_files:
            print(f"No files with the extension '{file_extension}' found in {directory_path}")

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Lab6/ex1.py <directory_path> <file_extension>")
    else:
        read_files_in_directory(sys.argv[1], sys.argv[2])


# python Lab6/ex1.py D:\University .txt
