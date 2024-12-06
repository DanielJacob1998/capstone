from flask import Blueprint, request, jsonify
from backend.utils.file_scanner import scan_directory
import atexit
import os
import json

file_bp = Blueprint('file', __name__)

# Global dictionary to track file metadata
file_details = {}

DETAILS_FILE = "file_details.json"

def save_details_to_file():
    try:
        print(f"Attempting to save details to {DETAILS_FILE}")
        with open(DETAILS_FILE, "w") as f:
            json.dump(file_details, f, indent=4)
        print(f"Details successfully saved to {DETAILS_FILE}")
    except Exception as e:
        print(f"Error saving details to {DETAILS_FILE}: {e}")

def load_details_from_file():
    global file_details
    if os.path.exists(DETAILS_FILE):
        with open(DETAILS_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    file_details.update(data)
                    print(f"Loaded file details: {file_details}")
                else:
                    print(f"Invalid data in {DETAILS_FILE}. Expected a dictionary.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {DETAILS_FILE}: {e}")

# Call this during startup
load_details_from_file()

# Call this before the app shuts down
atexit.register(save_details_to_file)

@file_bp.route("/scan", methods=["POST"])
def scan_files():
    data = request.json
    directory = data.get("directory")
    exclude_hidden = data.get("exclude_hidden", True)
    exclude_pyc = data.get("exclude_pyc", True)
    exclude_init = data.get("exclude_init", True)
    min_size = data.get("min_size")
    max_size = data.get("max_size")
    extensions = data.get("extensions")
    sort_by = data.get("sort_by", "file_name")
    sort_order = data.get("sort_order", "asc")

    try:
        files = list(
            scan_directory(
                directory,
                exclude_hidden=exclude_hidden,
                exclude_pyc=exclude_pyc,
                exclude_init=exclude_init,
                min_size=min_size,
                max_size=max_size,
                extensions=extensions,
            )
        )

        reverse_order = sort_order == "desc"
        if sort_by == "file_name":
            files.sort(key=lambda x: x.get("file_name", "").lower(), reverse=reverse_order)
        elif sort_by == "file_size":
            files.sort(key=lambda x: x.get("file_size", 0), reverse=reverse_order)
        elif sort_by in ["date_created", "date_modified", "date_accessed"]:
            files.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse_order)

        # Update file_details dictionary
        for file in files:
            ext = os.path.splitext(file["file_path"])[-1].lower()
            if ext not in file_details:
                file_details[ext] = []
            if file not in file_details[ext]:  # Avoid duplicates
                file_details[ext].append(file)

        # Debugging log
        print(f"Updated file details: {json.dumps(file_details, indent=4)}")

        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_bp.route("/save_details", methods=["POST"])
def save_details():
    save_details_to_file()
    return jsonify({"message": "File details saved successfully."})

@file_bp.route("/details", methods=["GET"])
def get_details():
    print(file_details)  # Or file_details if renamed
    return jsonify(file_details)
