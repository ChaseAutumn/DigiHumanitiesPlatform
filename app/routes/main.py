# app/routes/main.py

from flask import Blueprint, render_template, request
from app.utils.search_raw_data import search_raw_txt  # 引入搜索函数

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

        # 使用实际的搜索函数
        results = search_raw_txt(query)

        return render_template('search_raw_data.html', query=query, results=results)
    else:
        return render_template('search_raw_data.html')