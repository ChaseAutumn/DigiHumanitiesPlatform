# app/routes/main.py

from flask import Blueprint, render_template, request
from app.utils.search_raw_data import search_raw_txt
from app.utils.search_corrupt_sentence import search_corrupt_sentence  # 引入新的搜索函数
from app.utils.search_entity_sentences import search_entity_sentences  # 导入新的查询函数

# 定义 Blueprint
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return "About Page"


@main.route('/search_raw_data', methods=['GET', 'POST'])
def search_raw_data():
    if request.method == 'POST':
        query = request.form.get('query')
        results = search_raw_txt(query)
        return render_template('search_raw_data.html', query=query, results=results)
    else:
        return render_template('search_raw_data.html')


@main.route('/search_corrupt_sentence', methods=['GET', 'POST'])
def search_corrupt_sentence_route():
    if request.method == 'POST':
        query = request.form.get('query')
        results = search_corrupt_sentence(query)
        return render_template('search_corrupt_sentence.html', query=query, results=results)
    else:
        return render_template('search_corrupt_sentence.html')


@main.route('/search_entity_sentences', methods=['GET', 'POST'])
def search_entity_sentences_route():
    if request.method == 'POST':
        entity = request.form.get('entity')
        results = search_entity_sentences(entity)
        return render_template('search_entity_sentences.html', entity=entity, results=results)
    else:
        return render_template('search_entity_sentences.html')
