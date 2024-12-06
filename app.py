from flask import Flask
from flask_cors import CORS
from backend.routes.file_routes import file_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.register_blueprint(file_bp, url_prefix="/files")

    @app.route("/")
    def home():
        return "Welcome to the File Scanner API! Use /files/scan to scan directories."

    return app

app = create_app()

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
