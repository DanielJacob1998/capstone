from flask import Flask, jsonify
from backend.routes.file_routes import file_bp  # Import file scanner routes
from backend.routes.event_routes import event_bp  # Import event routes
from flask_cors import CORS  # Allow requests from frontend

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React frontend

# Register blueprints
app.register_blueprint(file_bp, url_prefix="/files")  # File scanner routes
app.register_blueprint(event_bp, url_prefix="/api/events")  # Events routes

# Placeholder for finances (will later be implemented as its own blueprint)
@app.route("/api/finances", methods=["GET", "POST"])
def finances():
    if request.method == "POST":
        data = request.json
        # Add logic to save financial data here
        return jsonify({"message": "Finance data saved successfully.", "data": data}), 201
    return jsonify({"message": "Finances API placeholder"})

# Default route
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Capstone API",
        "endpoints": {
            "File Scanner": "/files",
            "Events": "/api/events",
            "Finances": "/api/finances"
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
