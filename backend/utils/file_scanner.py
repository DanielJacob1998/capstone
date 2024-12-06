import os
from datetime import datetime
import humanize

def scan_directory(
    path, exclude_hidden=True, exclude_pyc=True, exclude_init=True,
    min_size=None, max_size=None, extensions=None
):
    try:
        for root, dirs, files in os.walk(path):
            if 'venv' in dirs:
                dirs.remove('venv')

            for file in files:
                if exclude_hidden and file.startswith('.'):
                    continue
                if exclude_pyc and file.endswith('.pyc'):
                    continue
                if exclude_init and file == '__init__.py':
                    continue
                if extensions and not any(file.lower().endswith(ext.lower()) for ext in extensions):
                    continue

                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                stat = os.stat(file_path)

                yield {
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "file_size": file_size,
                    "date_created": datetime.utcfromtimestamp(stat.st_ctime).isoformat(),
                    "date_modified": datetime.utcfromtimestamp(stat.st_mtime).isoformat(),
                    "date_accessed": datetime.utcfromtimestamp(stat.st_atime).isoformat(),
                }
    except Exception as e:
        raise Exception(f"Error scanning directory {path}: {e}")
