import os
import argparse

def scan_directory(path):
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    last_access_time = os.path.getatime(file_path)
                    yield file_path, file_size, last_access_time
                except OSError as e:
                    print(f"Error accessing {file_path}: {e}")
    except Exception as e:
        print(f"Error scanning directory {path}: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Scan a directory and list files.")
    parser.add_argument("directory", help="The path of the directory to scan")
    return parser.parse_args()

def main():
    args = parse_arguments()
    directory_path = args.directory
    for file_info in scan_directory(directory_path):
        print(file_info)

if __name__ == "__main__":
    main()
