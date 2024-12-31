from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime, timedelta

event_bp = Blueprint('event', __name__)
events_db = []  # In-memory database

# Helper Functions
def find_event(event_id):
    return next((event for event in events_db if event['id'] == event_id), None)

def validate_event(data):
    required_fields = ["title", "start_date", "end_date"]
    for field in required_fields:
        if not data.get(field):
            return f"{field} is required."
    try:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
        if end_date < start_date:
            return "End date cannot be before start date."
        if data.get("time"):
            datetime.strptime(data["time"], "%H:%M")
    except ValueError as e:
        return str(e)
    return None

def is_overlapping(start_date, end_date, time, group_id=None, subgroup_id=None, visibility="subgroup", exclude_event_id=None, user_id=None):
    for event in events_db:
        if exclude_event_id and event["id"] == exclude_event_id:
            continue
        if visibility == "subgroup" and event.get("subgroup_id") != subgroup_id:
            continue
        if visibility == "group" and event.get("group_id") != group_id:
            continue
        if event["created_by"] == user_id:  # Allow if same user created both events
            continue
        if (
            datetime.strptime(start_date, '%Y-%m-%d') <= datetime.strptime(event['end_date'], '%Y-%m-%d') and
            datetime.strptime(end_date, '%Y-%m-%d') >= datetime.strptime(event['start_date'], '%Y-%m-%d') and
            (not time or event.get('time') == time)
        ):
            return event
    return None

# Routes
@event_bp.route("/events", methods=["POST"])
def add_event():
    data = request.json
    if not data:
        return jsonify({"error": "No event data provided"}), 400

    # Validate input
    validation_error = validate_event(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    # Check for duplicate events
    for event in events_db:
        if (
            event["title"] == data["title"]
            and event["start_date"] == data["start_date"]
            and event.get("time") == data.get("time")
            and event.get("location") == data.get("location")
            and event.get("created_by") == data.get("user_id")
        ):
            return jsonify({
                "error": "Duplicate event. An identical event already exists.",
                "duplicate_event": event
            }), 409

    # Check for overlapping events
    force = data.get("force", False)
    overlapping_event = is_overlapping(
        data["start_date"],
        data["end_date"],
        data.get("time"),
        data.get("group_id"),
        data.get("subgroup_id"),
        data.get("visibility", "subgroup")
    )
    if overlapping_event and not force:
        return jsonify({
            "error": "Event overlaps with existing events",
            "conflicts": overlapping_event
        }), 409

    # Create the event
    event = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "description": data.get("description", ""),
        "start_date": data["start_date"],
        "end_date": data.get("end_date", data["start_date"]),
        "time": data.get("time", ""),
        "location": data.get("location", ""),
        "group_id": data.get("group_id"),
        "subgroup_id": data.get("subgroup_id"),
        "created_by": data["user_id"],
        "visibility": data.get("visibility", "group"),
    }
    events_db.append(event)
    return jsonify({"message": "Event created successfully", "event": event}), 201

@event_bp.route("/events", methods=["GET"])
def get_events():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    filtered_events = events_db
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            filtered_events = [
                event for event in events_db
                if start_date <= datetime.strptime(event["start_date"], "%Y-%m-%d") <= end_date
            ]
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'"}), 400

    start_index = (page - 1) * size
    end_index = start_index + size
    return jsonify({
        "events": filtered_events[start_index:end_index],
        "total": len(filtered_events),
        "page": page,
        "size": size
    }), 200
