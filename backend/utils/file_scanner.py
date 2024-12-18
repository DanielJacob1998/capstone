import os
from datetime import datetime
import humanize

def scan_directory(
    path, exclude_hidden=True, exclude_pyc=True, exclude_init=True,
    min_size=None, max_size=None, extensions=None,
    date_created_range=None, date_modified_range=None, date_accessed_range=None
):
    try:
        for root, dirs, files in os.walk(path):
            if 'venv' in dirs:
                dirs.remove('venv')

            for file in files:
                # Skip hidden files
                if exclude_hidden and file.startswith('.'):
                    continue
                if exclude_pyc and file.endswith('.pyc'):
                    continue
                if exclude_init and file == '__init__.py':
                    continue
                
                # Apply extensions filter
                if extensions:
                    file_extension = os.path.splitext(file)[1].lower()
                    if file_extension not in extensions:
                        continue

                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)

                # Check size filters
                if min_size and file_size < min_size:
                    continue
                if max_size and file_size > max_size:
                    continue

                # Fetch file times
                stat = os.stat(file_path)
                date_created = datetime.fromtimestamp(stat.st_ctime)
                date_modified = datetime.fromtimestamp(stat.st_mtime)
                date_accessed = datetime.fromtimestamp(stat.st_atime)

                # Check date ranges
                if date_created_range and not (date_created_range[0] <= date_created <= date_created_range[1]):
                    continue
                if date_modified_range and not (date_modified_range[0] <= date_modified <= date_modified_range[1]):
                    continue
                if date_accessed_range and not (date_accessed_range[0] <= date_accessed <= date_accessed_range[1]):
                    continue

                yield {
                    "file_path": file_path,
                    "file_size": file_size,
                    "date_created": date_created.strftime('%m/%d/%Y %H:%M:%S'),
                    "date_modified": date_modified.strftime('%m/%d/%Y %H:%M:%S'),
                    "date_accessed": date_accessed.strftime('%m/%d/%Y %H:%M:%S'),
                }
    except Exception as e:
        raise Exception(f"Error scanning directory {path}: {e}")
