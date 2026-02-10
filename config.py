"""
BillMaster Pro - Application Configuration
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'billmaster-pro-secret-key-2026')
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'billmaster.db')
    SCHEMA_PATH = os.path.join(BASE_DIR, 'backend', 'schema.sql')
    FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')


# Active config
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
