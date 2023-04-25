from bottle import run, route, template, TEMPLATE_PATH, static_file, request, redirect
import os
import json
import sqlite3
import hashlib

base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'views')
TEMPLATE_PATH.insert(0, views_path)

def read_categories():
    with sqlite3.connect('pingo.db') as conn:
        c = conn.cursor()
        data = c.fetchall()
        return data

@route("/")
def index():
    '''visar index.html'''
    return template("index")


@route('/categories')
def categories():
    with sqlite3.connect('pingo.db') as conn:
        c = conn.cursor()

        # Query the categories from the database
        c.execute('''SELECT category, challenges FROM categories''')
        data = c.fetchall()
        categories = []
    for row in data:
        category = {
            'category': row[0],
            'challenges': json.loads(row[1])
        }
        categories.append(category)

    return template('views/categories', data=categories)

@route('/bingo/<category>')
def bingo(category):
    categories = read_categories()
    challenges = []
    for item in categories:
        if item['category'] == category:
            challenges = item['challenges']
            break
    return template('views/bingo', data=challenges, category=category)


@route("/register", method=["GET"])
def register():
    return template('views/register')

@route("/register", method=["POST"])
def create_user():
    request.method == "POST"
    email = getattr(request.forms, ("email"))
    password = getattr(request.forms, ("password"))

    # Generate a hash of the password using SHA-256
    hash_obj = hashlib.sha256(password.encode())
    password_hash = hash_obj.hexdigest()

    # Insert the user data into the database
    with sqlite3.connect('pingo.db') as conn:
        c = conn.cursor()

        c.execute('''INSERT INTO users (email, password) VALUES (?, ?)''',
                  (email, password_hash))

    redirect("/")
        

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./views/static')


run(host='127.0.0.1', port=8080, reloader=True, debug=True)
