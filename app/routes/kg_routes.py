# app/routes/kg_routes.py

from flask import Blueprint, render_template, request, jsonify
from app.utils.traverse_kg_new import load_kg, traverse_kg_depth_new

# 定义 Blueprint
kg_routes = Blueprint('kg_routes', __name__)

# 知识图谱文件路径
from app.utils.traverse_kg_new import KG_FILEPATH

@kg_routes.route('/api/get_subgraph', methods=['GET'])
def get_subgraph():
    entity = request.args.get('entity')
    depth = request.args.get('depth', type=int, default=1)

    kg = load_kg(KG_FILEPATH)
    if kg is None:
        return jsonify({'error': '知识图谱未加载'}), 500

    subgraph = traverse_kg_depth_new(kg, entity, depth)
    if not subgraph['nodes']:
        return jsonify({'error': f"实体 '{entity}' 不存在或没有相关数据。"}), 404

    return jsonify(subgraph)

@kg_routes.route('/show_subgraph')
def show_subgraph():
    return render_template('show_subgraph.html.jinja2')