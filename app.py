from flask import Flask
from backend.routes.file_routes import file_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(file_bp, url_prefix="/files")

    # Add a route for '/'
    @app.route("/")
    def home():
        return "Welcome to the File Scanner API! Use /files/scan to scan directories."

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
