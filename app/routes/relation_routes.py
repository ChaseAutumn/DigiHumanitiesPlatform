# app/routes/relation_routes.py

from flask import Blueprint, render_template, request
from app.utils.search_relation_sentences import search_relation_sentences

# 定义 Blueprint
relation_routes = Blueprint('relation_routes', __name__)

@relation_routes.route('/search_relation_sentences', methods=['GET', 'POST'])
def search_relation_sentences_route():
    if request.method == 'POST':
        relation = request.form.get('relation')
        results = search_relation_sentences(relation)
        return render_template('search_relation_sentences.html.jinja2', relation=relation, results=results)
    else:
        return render_template('search_relation_sentences.html.jinja2')