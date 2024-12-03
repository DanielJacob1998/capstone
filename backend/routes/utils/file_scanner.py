import os

def scan_directory(path):
    try:
        for root, dirs, files in os.walk(path):
            for name in dirs:
                dir_path = os.path.join(root, name)
                yield {
                    "path": dir_path,
                    "type": "directory",
                    "size": None,
                    "last_access_time": None
                }
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    last_access_time = os.path.getatime(file_path)
                    yield {
                        "path": file_path,
                        "type": "file",
                        "size": file_size,
                        "last_access_time": last_access_time
                    }
                except OSError as e:
                    print(f"Error accessing {file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error scanning directory {path}: {e}")
