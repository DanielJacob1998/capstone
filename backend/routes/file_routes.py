from flask import Blueprint, request, jsonify
from backend.utils.file_scanner import scan_directory

file_bp = Blueprint('file', __name__)

@file_bp.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()

    # Get directory path from the request
    directory = data.get('directory')
    if not directory:
        return jsonify({"error": "Directory path is required"}), 400

    # Optional filters
    exclude_hidden = data.get('exclude_hidden', True)
    exclude_pyc = data.get('exclude_pyc', True)
    exclude_init = data.get('exclude_init', True)

    # Optional sorting by file_size or last_access_time
    sort_by = data.get('sort_by', 'file_size')  # Default is by file size
    sort_order = data.get('sort_order', 'desc')  # 'asc' or 'desc'

    try:
        # No file_type filter now, all files will be included
        files = list(scan_directory(directory, exclude_hidden, exclude_pyc, exclude_init))

        # Sorting by file_size or last_access_time
        if sort_by == 'file_size':
            files.sort(key=lambda x: x['file_size'], reverse=(sort_order == 'desc'))
        elif sort_by == 'last_access_time':
            files.sort(key=lambda x: x['last_access_time'], reverse=(sort_order == 'desc'))

        return jsonify(files), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_bp.route('/files/scan', methods=['POST'])
def scan_files():
    data = request.json
    print("Received request payload:", data)
    
    directory = data.get('directory')
    if not directory:
        return jsonify({"error": "Directory path is required"}), 400
    
    print("Scanning directory:", directory)
    try:
        files = scan_directory(directory, data.get('exclude_hidden', True), data.get('exclude_pyc', True), data.get('exclude_init', True))
        print("Files scanned:", files)
        return jsonify(files)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
