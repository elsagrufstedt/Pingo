from bottle import run, route, template, TEMPLATE_PATH, static_file
import os
import json

base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'views')
TEMPLATE_PATH.insert(0, views_path)


def read_categories():
    try:
        with open('views/static/categories.json', 'r',  encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        with open('views/static/categories.json', 'w') as f:
            f.write(json.dumps([]))
            return []


@route("/")
def index():
    '''visar index.html'''
    return template("index")


@route('/categories')
def categories():
    data = read_categories()
    return template('views/categories', data=data)


@route('/bingo/<category>')
def bingo(category):
    data = read_categories()
    for item in data:
        if item['category'] == category:
            return template('views/bingo', data=item['challenges'], category=category)


@route('/login')
def login():
    return template('views/login')


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./views/static')


run(host='127.0.0.1', port=8080, reloader=True, debug=True)
