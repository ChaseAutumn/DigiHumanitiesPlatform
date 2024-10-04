# app/routes/__init__.py

from .main import main
from .kg_routes import kg_routes  # 导入新的路由
from .relation_routes import relation_routes  # 导入新的路由


# 注册 Blueprint
def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(kg_routes)
    app.register_blueprint(relation_routes)