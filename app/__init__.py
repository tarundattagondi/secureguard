from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so they're registered
    from app import models  # noqa: F401
    # Register blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.controls import controls_bp
    from app.routes.risks import risks_bp
    from app.routes.scans import scans_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(controls_bp)
    app.register_blueprint(risks_bp)
    app.register_blueprint(scans_bp)

    return app

