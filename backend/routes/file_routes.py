from flask import Blueprint, request, jsonify
from backend.utils.file_scanner import scan_directory

file_bp = Blueprint('file', __name__)

@file_bp.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    directory = data.get('directory')

    if not directory:
        return jsonify({"error": "Directory path is required"}), 400

    try:
        files = list(scan_directory(directory))
        return jsonify(files), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

