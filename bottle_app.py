from bottle import run, route, template, TEMPLATE_PATH, static_file
import os

base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'views')
TEMPLATE_PATH.insert(0, views_path)


@route("/")
def index():
    '''visar index.html'''
    return template("index")


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./views/static')


run(host='127.0.0.1', port=8080, reloader=True)
