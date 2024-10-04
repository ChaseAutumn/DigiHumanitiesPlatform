# app/__init__.py

from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import register_blueprints
    register_blueprints(app)

    return app