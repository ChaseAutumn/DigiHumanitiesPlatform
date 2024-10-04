# app/__init__.py

from flask import Flask
from config import Config
import re

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import register_blueprints
    register_blueprints(app)

    # 定义自定义过滤器
    @app.template_filter('replace_regex')
    def replace_regex(s, pattern, repl):
        return re.sub(pattern, repl, s)

    return app