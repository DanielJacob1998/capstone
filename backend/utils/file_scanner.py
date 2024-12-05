import os
from datetime import datetime
import humanize

def scan_directory(
    path, exclude_hidden=True, exclude_pyc=True, exclude_init=True, min_size=None, max_size=None
):
    """
    Scan a directory and yield files with their details.

    Parameters:
    - path (str): Directory path to scan.
    - exclude_hidden (bool): Exclude hidden files (like .DS_Store).
    - exclude_pyc (bool): Exclude .pyc files.
    - exclude_init (bool): Exclude __init__.py files.
    - min_size (int): Minimum file size in bytes.
    - max_size (int): Maximum file size in bytes.

    Returns:
    - Generator: Yields file details (path, size, last access time).
    """
    try:
        for root, dirs, files in os.walk(path):
            if 'venv' in dirs:
                dirs.remove('venv')  # Prevent os.walk from descending into 'venv'

            for file in files:
                if exclude_hidden and file.startswith('.'):
                    continue
                if exclude_pyc and file.endswith('.pyc'):
                    continue
                if exclude_init and file == '__init__.py':
                    continue

                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)  # Get size in bytes

                # Filter by file size range
                if min_size and file_size < min_size:
                    continue
                if max_size and file_size > max_size:
                    continue

                try:
                    # Format last access time
                    last_access_time = os.path.getatime(file_path)
                    formatted_time = datetime.utcfromtimestamp(last_access_time).strftime('%m/%d/%Y %H:%M:%S')

                    # Yield the raw file size for proper sorting
                    yield {
                        "file_path": file_path,
                        "file_size": file_size,  # Raw size in bytes
                        "formatted_size": humanize.naturalsize(file_size),  # Human-readable size
                        "last_access_time": formatted_time,
                    }
                except OSError as e:
                    print(f"Error accessing {file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error scanning directory {path}: {e}")
