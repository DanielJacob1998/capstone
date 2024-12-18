from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime

event_bp = Blueprint('event', __name__)

# In-memory database for events
events_db = []

# Helper function to find an event by ID
def find_event(event_id):
    for event in events_db:
        if event['id'] == event_id:
            return event
    return None

# Get all events or filter by date range
@event_bp.route('/events', methods=['GET'])
def get_events():
    start_date = request.args.get('start_date')  # e.g., '2024-12-01'
    end_date = request.args.get('end_date')      # e.g., '2024-12-31'
    
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            filtered_events = [
                event for event in events_db
                if start_date <= datetime.strptime(event['start_date'], '%Y-%m-%d') <= end_date
            ]
            return jsonify(filtered_events), 200
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'"}), 400

    return jsonify(events_db), 200

# Create a new event
@event_bp.route('/events', methods=['POST'])
def add_event():
    data = request.json
    if not data or not data.get("title") or not data.get("start_date"):
        return jsonify({"error": "Title and start date are required"}), 400

    event = {
        'id': str(uuid.uuid4()),  # Unique event ID
        'title': data['title'],
        'description': data.get('description', ''),
        'start_date': data['start_date'],  # Format: 'YYYY-MM-DD'
        'end_date': data.get('end_date', data['start_date']),  # Default to start_date
        'time': data.get('time', ''),  # Format: 'HH:MM'
        'location': data.get('location', ''),
    }
    events_db.append(event)
    return jsonify({"message": "Event created successfully", "event": event}), 201

# Update an existing event
@event_bp.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    data = request.json
    event.update({
        'title': data.get('title', event['title']),
        'description': data.get('description', event['description']),
        'start_date': data.get('start_date', event['start_date']),
        'end_date': data.get('end_date', event['end_date']),
        'time': data.get('time', event['time']),
        'location': data.get('location', event['location']),
    })
    return jsonify({"message": "Event updated successfully", "event": event}), 200

# Delete an event
@event_bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events_db
    event = find_event(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    events_db = [e for e in events_db if e['id'] != event_id]
    return jsonify({"message": "Event deleted successfully"}), 200
