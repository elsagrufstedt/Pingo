from bottle import run, route, template, TEMPLATE_PATH
import os

base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'views')
TEMPLATE_PATH.insert(0, views_path)

@route("/")
def index():
    '''visar index.html'''
    return template("index")

run(host='127.0.0.1', port=8080, reloader=True)