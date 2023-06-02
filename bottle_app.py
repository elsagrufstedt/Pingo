from bottle import (
    run, route, template, TEMPLATE_PATH, static_file,
    request, redirect, default_app, hook, response
)
import os
import sqlite3
import hashlib
from beaker.middleware import SessionMiddleware

from config import API_URL

@hook('after_request')
def set_api_cookie():
    '''
        Sätter den URL som vi vill skicka vårt resultat till för livescore.
        URL hämtas från filen "config.py"
    '''
    # Sets the URL to the Website for livescore from "config.py" (when start page is loade)
    response.set_header('Set-Cookie', 'API_URL='+API_URL)

#base_path = os.path.abspath(os.path.dirname(__file__))
#views_path = os.path.join(base_path, 'views')
#TEMPLATE_PATH.insert(0, views_path)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

application = default_app()
app = SessionMiddleware(application, session_opts)

def connect_database():
    return sqlite3.connect('/home/peggydelvret/mysite/pingo.db')

def authenticate(email, password):
    with connect_database() as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM Users WHERE email=?", (email,))
        result = c.fetchone()
        if result:
            stored_password = result[0]
            hash_obj = hashlib.sha256(password.encode())
            password_hash = hash_obj.hexdigest()
            if password_hash == stored_password:
                return True
    return False


@route("/")
def index():
    session = request.environ.get('beaker.session')
    if 'email' in session:
        conn = connect_database()
        c = conn.cursor()
        c.execute("SELECT username FROM Users WHERE email=?", (session['email'],))
        result = c.fetchone()
        if result:
            username = result[0]
            return template("index_log", username=username)
    return template("index")

@route('/categories')
def categories():
    with connect_database() as conn:
        c = conn.cursor()

        c.execute('''SELECT category_name FROM Categories WHERE user_id = (
                     SELECT id FROM Users WHERE email=?) AND is_premade = 0''',
                  (request.environ.get('beaker.session').get('email'),))
        data = c.fetchall()
        categories = [{'category': row[0]} for row in data]

        c.execute("SELECT category_name FROM Categories WHERE is_premade = 1")
        premade_data = c.fetchall()
        premade_categories = [{'category': row[0]} for row in premade_data]

    return template('views/categories', data=categories, premade_categories=premade_categories)


@route('/bingo/<category>')
def bingo(category):
    conn = connect_database()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''SELECT challenge_name FROM Challenges
                 WHERE category_id = (
                 SELECT id FROM Categories WHERE category_name = ?)''', (category,))
    challenges = [row['challenge_name'] for row in c.fetchall()]

    conn.close()

    print(challenges)

    hour = request.query.get('hour')
    minute = request.query.get('minute')
    second = request.query.get('second')
    return template('/home/peggydelvret/mysite/views/bingo', data=challenges, category=category, hour=hour, minute=minute, second=second)

@route("/register", method=["GET"])
def register():
    return template('views/register')

@route("/register", method=["POST"])
def register_user():
    email = getattr(request.forms,'email')
    password = getattr(request.forms,'password')
    username = getattr(request.forms, 'username')
    hash_obj = hashlib.sha256(password.encode())
    password_hash = hash_obj.hexdigest()

    with connect_database() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO Users (username, email, password) VALUES (?, ?, ?)''',
                  (username, email, password_hash))

    session = request.environ.get('beaker.session')
    session['email'] = email
    session.save()

    redirect("/")

@route("/login", method=["GET"])
def login():
    return template('views/login')

@route("/login", method=["POST"])
def login_user():
    email = getattr(request.forms,'email')
    password = getattr(request.forms,'password')

    if authenticate(email, password):
        session = request.environ.get('beaker.session')
        session['email'] = email
        session.save()
        redirect("/")
    else:
        return "Invalid credentials"

@route('/start/<category>')
def start(category):
    conn = sqlite3.connect('pingo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT challenge_name FROM Challenges
                 WHERE category_id = (SELECT id FROM Categories WHERE category_name = ?)''', (category,))
    challenges = [row['challenge_name'] for row in c.fetchall()]
    conn.close()
    return template('/home/peggydelvret/mysite/views/start', data=challenges, category=category)


@route('/starting/<category>', method='POST')
def starting_game(category):
    conn = sqlite3.connect('pingo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT challenge_name FROM Challenges
                 WHERE category_id = (SELECT id FROM Categories WHERE category_name = ?)''', (category,))
    challenges = [row['challenge_name'] for row in c.fetchall()]
    conn.close()
    hour = getattr(request.forms, 'hour')
    minute = getattr(request.forms, 'minute')
    second = getattr(request.forms, 'second')
    redirect('/bingo/{}?hour={}&minute={}&second={}'.format(category, hour, minute, second))

#Gör inget just nu
@route('/profile')
def profile():
    return template('views/profile')

@route('/logout')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    redirect('/')

@route('/add', method="GET")
def add():
    if 'email' not in request.environ.get('beaker.session'):
        redirect('/login')

    return template("views/add")

@route('/add', method="POST")
def add_new():
    if 'email' not in request.environ.get('beaker.session'):
        redirect('/login')

    conn = connect_database()
    c = conn.cursor()
    category_name = getattr(request.forms,'category')
    user_email = request.environ.get('beaker.session')['email']
    c.execute("INSERT INTO Categories (category_name, user_id) VALUES (?, (SELECT id FROM Users WHERE email=?))",
              (category_name, user_email))
    category_id = c.lastrowid
    challenges = [getattr(request.forms,f'challenge_{i}') for i in range(1, 26)]
    c.executemany("INSERT INTO Challenges (category_id, challenge_name) VALUES (?, ?)",
                  ((category_id, challenge_name) for challenge_name in challenges))
    conn.commit()
    conn.close()
    redirect("/categories")

@route('/remove', method='POST')
def remove_category():
    if 'email' not in request.environ.get('beaker.session'):
        redirect('/login')

    category_name = getattr(request.forms,'category_name')

    conn = connect_database()
    c = conn.cursor()

    c.execute("DELETE FROM Categories WHERE category_name=? AND user_id=(SELECT id FROM Users WHERE email=?)",
              (category_name, request.environ.get('beaker.session')['email']))
    conn.commit()
    conn.close()
    redirect('/categories')

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/peggydelvret/mysite//views/static')

application = default_app()

# run(app=app, host='127.0.0.1', port=8080, reloader=True, debug=True)