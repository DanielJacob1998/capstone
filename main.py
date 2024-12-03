import os
import argparse

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
