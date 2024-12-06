import os
from datetime import datetime
import humanize

def scan_directory(
    path, exclude_hidden=True, exclude_pyc=True, exclude_init=True,
    min_size=None, max_size=None, extensions=None
):
    """
    Scans the directory and yields file details including name, size, and timestamps.
    """
    try:
        for root, dirs, files in os.walk(path):
            # Skip unwanted directories
            if 'venv' in dirs:
                dirs.remove('venv')

            for file in files:
                file_path = os.path.join(root, file)

                # Skip excluded files
                if exclude_hidden and file.startswith('.'):
                    continue
                if exclude_pyc and file.endswith('.pyc'):
                    continue
                if exclude_init and file == '__init__.py':
                    continue

                # Filter by extensions
                if extensions and not any(file.lower().endswith(ext.lower()) for ext in extensions):
                    continue

                # Get file attributes
                file_size = os.path.getsize(file_path)
                date_accessed = datetime.utcfromtimestamp(os.path.getatime(file_path))
                date_modified = datetime.utcfromtimestamp(os.path.getmtime(file_path))
                date_created = datetime.utcfromtimestamp(os.path.getctime(file_path))

                # Filter by size
                if min_size and file_size < min_size:
                    continue
                if max_size and file_size > max_size:
                    continue

                # Yield file details
                yield {
                    "file_name": file,
                    "file_path": file_path,
                    "file_size": file_size,
                    "date_accessed": date_accessed.strftime('%m/%d/%Y %H:%M:%S'),
                    "date_modified": date_modified.strftime('%m/%d/%Y %H:%M:%S'),
                    "date_created": date_created.strftime('%m/%d/%Y %H:%M:%S'),
                }
    except Exception as e:
        raise Exception(f"Error scanning directory {path}: {e}")
