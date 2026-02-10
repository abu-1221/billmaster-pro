"""
BillMaster Pro - Flask Application Factory
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from backend.database import init_db
from backend.seed import seed_database
from backend.routes import register_routes


def create_app(app_config):
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder=None)
    app.config.from_object(app_config)

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Initialize Database
    db_manager = init_db(app_config)

    # Seed Database if needed
    with app.app_context():
        invoices_seeded = seed_database(db_manager)
        if invoices_seeded:
            print(f"✅ Database seeded with {invoices_seeded} sample invoices")

    # Register API Routes
    register_routes(app)

    # Serve static frontend files
    @app.route('/')
    def index():
        return send_from_directory(app.config['FRONTEND_DIR'], 'index.html')

    @app.route('/<path:path>')
    def serve_frontend(path):
        # Check if the file exists in the frontend directory
        if os.path.exists(os.path.join(app.config['FRONTEND_DIR'], path)):
            return send_from_directory(app.config['FRONTEND_DIR'], path)
        # Otherwise, serve index.html (for client-side routing if any, 
        # but here we just serve the file or 404)
        return send_from_directory(app.config['FRONTEND_DIR'], 'index.html')

    return app
