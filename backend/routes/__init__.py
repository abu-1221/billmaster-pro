"""BillMaster Pro - Routes Package"""

from flask import Blueprint


def register_routes(app):
    """Register all API route blueprints."""
    from backend.routes.auth import auth_bp
    from backend.routes.categories import categories_bp
    from backend.routes.products import products_bp
    from backend.routes.customers import customers_bp
    from backend.routes.invoices import invoices_bp
    from backend.routes.analytics import analytics_bp
    from backend.routes.settings import settings_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(customers_bp, url_prefix='/api')
    app.register_blueprint(invoices_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    app.register_blueprint(settings_bp, url_prefix='/api')
