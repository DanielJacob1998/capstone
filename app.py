from flask import Flask, jsonify
from backend.routes.file_routes import file_bp
from backend.routes.event_routes import event_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(file_bp, url_prefix="/files")
app.register_blueprint(event_bp, url_prefix="/api")

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
