import sys
from pathlib import Path

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask
from backend.routes.file_routes import file_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(file_bp, url_prefix="/files")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
