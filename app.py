"""
BillMaster Pro - Main Flask Application
Billing & Institute Management System
Python/Flask Backend - Vercel Serverless Compatible
"""

from flask import Flask, redirect, session, send_from_directory, jsonify
from flask_cors import CORS
import os

# Import route blueprints
from routes.auth import auth_bp
from routes.categories import categories_bp
from routes.customers import customers_bp
from routes.products import products_bp
from routes.invoices import invoices_bp
from routes.analytics import analytics_bp
from routes.settings import settings_bp

# Initialize Flask app
app = Flask(__name__, static_folder='.')
app.secret_key = os.environ.get('SECRET_KEY', 'billmaster_pro_secret_key_2024')

# Session configuration - Use cookies for serverless
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True if os.environ.get('VERCEL') else False

# Try to use Flask-Session, fallback to basic sessions
try:
    from flask_session import Session
    Session(app)
except:
    pass  # Use default Flask sessions

# Enable CORS for all domains with credentials
CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept", "X-Requested-With"]
    }
})

# Register blueprints with /api prefix
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(categories_bp, url_prefix='/api')
app.register_blueprint(customers_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(invoices_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(settings_bp, url_prefix='/api')

# Main entry point - redirect based on login status
@app.route('/')
def index():
    """Redirect to dashboard or login based on session"""
    if session.get('logged_in'):
        return redirect('/dashboard.html')
    return redirect('/login.html')

# Serve static files (HTML, CSS, JS, etc.)
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from the project directory"""
    try:
        return send_from_directory('.', filename)
    except:
        return redirect('/login.html')

# Health check endpoint for Vercel
@app.route('/api/health')
def health_check():
    return jsonify({'status': 'ok', 'message': 'BillMaster Pro is running'})

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return redirect('/login.html')

@app.errorhandler(500)
def server_error(e):
    return {'success': False, 'message': 'Internal server error'}, 500

# For local development
if __name__ == '__main__':
    print("=" * 60)
    print("  BillMaster Pro - Python/Flask Backend")
    print("  Billing & Institute Management System")
    print("=" * 60)
    print()
    print("  Starting server at: http://127.0.0.1:5000")
    print("  API Endpoints at:   http://127.0.0.1:5000/api/")
    print()
    print("  Default Admin Login:")
    print("    Username: admin")
    print("    Password: admin123")
    print()
    print("=" * 60)
    
    # Run the development server
    app.run(host='0.0.0.0', port=5000, debug=True)
