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
        c.execute('''SELECT category_name FROM Categories''')
        data = c.fetchall()
        categories = []
    for row in data:
        category = {
            'category': row[0]
        }
        categories.append(category)

    return template('views/categories', data=categories)

@route('/bingo/<category>')
def bingo(category):
    # Connect to database
    conn = sqlite3.connect('pingo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Retrieve challenges for the selected category
    c.execute('''SELECT challenge_name FROM Challenges
                 WHERE category_id = (SELECT id FROM Categories WHERE category_name = ?)''', (category,))
    challenges = [row['challenge_name'] for row in c.fetchall()]

    # Close database connection
    conn.close()

    return template('views/bingo', data=challenges, category=category)



@route("/register", method=["GET"])
def register():
    return template('views/register')

@route("/register", method=["POST"])
def register_user():
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