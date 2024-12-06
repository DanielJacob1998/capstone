from flask import Blueprint, request, jsonify
from backend.utils.file_scanner import scan_directory
import atexit
import os
import json

file_bp = Blueprint('file', __name__)

# Global dictionary to track searched extensions and their files
searched_extensions = {}

EXTENSIONS_FILE = "extensions.json"

def save_extensions_to_file():
    try:
        with open(EXTENSIONS_FILE, "w") as f:
            json.dump(searched_extensions, f, indent=4)  # Add `indent=4` for readability
    except Exception as e:
        print(f"Error saving extensions to {EXTENSIONS_FILE}: {e}")

def load_extensions_from_file():
    global searched_extensions
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as f:
            try:
                data = json.load(f)
                # Validate that the loaded data is a dictionary
                if isinstance(data, dict):
                    searched_extensions.update(data)
                else:
                    print(f"Invalid data in {EXTENSIONS_FILE}. Expected a dictionary.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {EXTENSIONS_FILE}: {e}")

# Call this during startup
load_extensions_from_file()

# Call this before the app shuts down
atexit.register(save_extensions_to_file)

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

    try:
        scanned_files = list(
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

        # Add file paths to `searched_extensions` only if they match
        if extensions:
            for file in scanned_files:
                for ext in extensions:
                    if file["file_path"].endswith(ext):
                        # Initialize the extension list if not already present
                        if ext not in searched_extensions:
                            searched_extensions[ext] = []
                        # Add the file path if not already present
                        if file["file_path"] not in searched_extensions[ext]:
                            searched_extensions[ext].append(file["file_path"])

        # Sort files by size (default if no sort_by is specified)
        scanned_files.sort(key=lambda x: x["file_size"], reverse=True)

        return jsonify(scanned_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_bp.route("/save_extensions", methods=["POST"])
def save_extensions():
    save_extensions_to_file()
    return jsonify({"message": "Extensions saved successfully."})


@file_bp.route("/extensions/details", methods=["GET"])
def get_extensions_details():
    return jsonify({
        ext: searched_extensions[ext]
        for ext in searched_extensions
    })
