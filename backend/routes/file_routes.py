from flask import Blueprint, request, jsonify, current_app
from ics import Calendar
from datetime import datetime
from icalendar import Calendar
import csv
import io
import os
import requests
import logging

# Initialize Blueprint
file_bp = Blueprint('file', __name__)
BASE_API_URL = os.getenv("BASE_API_URL", "http://127.0.0.1:5000")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# In-memory cache to track scanned files (optional)
scanned_files_cache = set()

# Helper Function: Validate Date
def validate_date(date_str):
    """Validates and parses a date string."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected format 'YYYY-MM-DD'.")

# Helper Function: Validate Event Data
def validate_event_data(event):
    required_fields = ["title", "start_date"]
    for field in required_fields:
        if not event.get(field):
            return f"Missing required field: {field}"

    try:
        start_date = validate_date(event["start_date"])
        end_date = validate_date(event.get("end_date", event["start_date"]))
        if end_date < start_date:
            return "End date cannot be before start date."
    except ValueError as e:
        return str(e)

    return None

@file_bp.route('/parse-calendar', methods=['POST'])
def parse_calendar_file():
    """Endpoint to parse a calendar file (.ics)."""
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    if not file.filename.lower().endswith('.ics'):
        return jsonify({"error": "Unsupported file format. Only .ics files are allowed."}), 400

    try:
        # Use icalendar for parsing
        content = file.stream.read()
        calendar = Calendar.from_ical(content)
        parsed_events = []

        for component in calendar.walk():
            if component.name == "VEVENT":
                try:
                    event = {
                        "title": str(component.get("SUMMARY", "")),
                        "description": str(component.get("DESCRIPTION", "")),
                        "start_date": component.get("DTSTART").dt.isoformat(),
                        "end_date": component.get("DTEND").dt.isoformat() if component.get("DTEND") else None,
                        "time": component.get("DTSTART").dt.strftime("%H:%M") if hasattr(component.get("DTSTART").dt, "strftime") else "",
                        "location": str(component.get("LOCATION", "")),
                    }
                    parsed_events.append(event)
                except Exception as e:
                    current_app.logger.error(f"Error parsing event: {e}")

        # Send parsed events to the calendar API
        results = process_events(parsed_events)
        return jsonify({
            "message": "Calendar file parsed successfully.",
            "parsed_events": parsed_events,
            "results": results,
        }), 200

    except Exception as e:
        current_app.logger.error(f"Failed to parse calendar file: {str(e)}")
        return jsonify({"error": f"Failed to parse calendar file: {str(e)}"}), 500

# Helper Function: Log and Handle API Errors
def process_events(events):
    errors = []
    successes = []
    for index, event in enumerate(events):
        # Validate the event
        validation_error = validate_event_data(event)
        if validation_error:
            logger.error(f"Validation failed for event {event['title']}: {validation_error}")
            errors.append({"event_row": index + 1, "event": event, "error": validation_error})
            continue

        # Send event to API
        response = requests.post(f"{BASE_API_URL}/api/events", json=event)
        if response.status_code != 201:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = {"error": "Invalid response from event API"}
            logger.error(f"Failed to create event {event['title']}: {error_detail}")
            errors.append({"event_row": index + 1, "event": event, "error": error_detail})
        else:
            successes.append(event)
            logger.info(f"Successfully created event: {event['title']}")

    return {"successes": successes, "errors": errors}

# Route: Scan Directory
@file_bp.route('/scan', methods=['POST'])
def scan_directory():
    """Scan directory and parse relevant files."""
    data = request.json
    directory = data.get('directory')
    extensions = data.get('extensions', [])

    if not directory:
        return jsonify({"error": "Directory is required"}), 400

    if not os.path.exists(directory) or not os.path.isdir(directory):
        return jsonify({"error": "Directory does not exist or is not accessible"}), 400

    parsed_events = []
    errors = []

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if not extensions or any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    if file.lower().endswith(".ics"):
                        events = parse_ics(file_path)
                        if isinstance(events, list):
                            parsed_events.extend(events)
                        else:
                            errors.append({"file": file, "error": events.get("error")})
                    # Handle other extensions like CSV if needed here

        return jsonify({
            "message": f"Scanned and parsed files in {directory}",
            "parsed_events": parsed_events,
            "errors": errors,
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to scan and parse directory: {str(e)}"}), 500

@file_bp.route('/parse-finance', methods=['POST'])
def parse_finance_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "Unsupported file format. Only .csv files are allowed."}), 400

    try:
        transactions = []
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)

        for index, row in enumerate(reader, start=1):
            try:
                # Validate and parse each transaction
                date = validate_date(row["Date"])
                amount = float(row["Amount"])  # Ensures valid float
                category = row.get("Category", "Uncategorized")
                description = row.get("Description", "")
                user_id = request.form.get("user_id") or "default_user"

                transaction = {
                    "date": date.isoformat(),
                    "amount": amount,
                    "category": category,
                    "description": description,
                    "user_id": user_id,
                }

                transactions.append(transaction)

            except KeyError as e:
                current_app.logger.error(f"Missing required field in row {index}: {e}")
            except ValueError as e:
                current_app.logger.error(f"Invalid data format in row {index}: {e}")

        # Batch processing of transactions
        return process_financial_transactions(transactions)

    except Exception as e:
        current_app.logger.error(f"Failed to parse file: {str(e)}")
        return jsonify({"error": f"Failed to parse file: {str(e)}"}), 500

def process_financial_transactions(transactions):
    """Sends transactions to the finance API in batches."""
    errors = []
    for transaction in transactions:
        response = requests.post(f"{BASE_API_URL}/api/finances", json=transaction)
        if response.status_code != 201:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = {"error": "Invalid response from finance API"}
            errors.append({"transaction": transaction, "error": error_detail})

    if errors:
        return jsonify({
            "message": "Some transactions could not be created.",
            "errors": errors,
        }), 207

    return jsonify({"message": "All transactions added successfully."}), 201
