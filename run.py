"""
BillMaster Pro - Execution Entry Point
"""

import os
from backend.app import create_app
from config import config

# Determine environment
env = os.environ.get('FLASK_ENV', 'development')
app_config = config.get(env, config['default'])

# Create app
app = create_app(app_config)

if __name__ == '__main__':
    print(f"🚀 BillMaster Pro starting in {env} mode")
    print(f"🔗 Access the application at: http://{app_config.HOST}:{app_config.PORT}")
    print("=" * 50)
    app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        debug=app_config.DEBUG
    )
