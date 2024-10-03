from flask import Flask

def create_app():
    app = Flask(__name__)

    # 从 routes 导入 main 并注册
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app