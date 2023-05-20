from bottle import run, route, template, TEMPLATE_PATH, static_file, request, redirect
import os
import sqlite3
import hashlib


base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'views')
TEMPLATE_PATH.insert(0, views_path)

def get_category_from_database():
    '''Ska hämta kategorierna från databasen'''
    conn = sqlite3.connect('pingo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT category_name FROM Categories")
    categories = [row['category_name'] for row in c.fetchall()]
    conn.close()

    return categories

@route("/")
def index():
    '''visar index.html'''
    return template("index")


@route('/categories')
def categories():
    conn = sqlite3.connect('pingo.db')
    c = conn.cursor()
    c.execute('''SELECT category_name FROM Categories''')
    data = c.fetchall()
    categories = []
    for row in data:
        category = {
            'category': row[0],
            'remove_link': f'/remove-category/{row[0]}'
        }
        categories.append(category)

    return template('views/categories', data=categories)


@route('/bingo/<category>')
def bingo(category):
    conn = sqlite3.connect('pingo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT challenge_name FROM Challenges
                 WHERE category_id = (SELECT id FROM Categories WHERE category_name = ?)''', (category,))
    challenges = [row['challenge_name'] for row in c.fetchall()]

    conn.close()

    hour = request.query.get('hour')
    minute = request.query.get('minute')
    second = request.query.get('second')

    return template('views/bingo', data=challenges, category=category, hour=hour, minute=minute, second=second)


@route('/add', method="GET")
def add():
    return template("views/add")


@route('/add', method="POST")
def add_new():
    conn = sqlite3.connect('pingo.db')
    c = conn.cursor()
    category_name = getattr(request.forms, 'category')
    c.execute("INSERT INTO Categories (category_name) VALUES (?)",
              (category_name,))
    category_id = c.lastrowid

    challenges = []
    for i in range(1, 26):
        challenge_name = getattr(request.forms, f'challenge_{i}')
        challenges.append(challenge_name)

    for challenge_name in challenges:
        c.execute("INSERT INTO Challenges (category_id, challenge_name) VALUES (?,?)",
                  (category_id, challenge_name))
    conn.commit()
    conn.close()
    redirect("/categories")


@route('/remove-category/<category>')
def remove_category(category):
    conn = sqlite3.connect('pingo.db')
    c = conn.cursor()
    c.execute('''DELETE FROM Challenges
                 WHERE category_id = (SELECT id FROM Categories WHERE category_name = ?)''', (category,))
    
    c.execute('''DELETE FROM Categories WHERE category_name = ?''', (category,))
    conn.commit()
    conn.close()

    redirect("/categories")



@route("/register", method="GET")
def register():
    return template('views/register')


@route("/register", method="POST")
def register_user():
    email = getattr(request.forms, ("email"))
    password = getattr(request.forms, ("password"))
    hash_obj = hashlib.sha256(password.encode())
    password_hash = hash_obj.hexdigest()
    conn = sqlite3.connect('pingo.db')
    c = conn.cursor()

    c.execute('''SELECT email FROM Users WHERE email = ?''', (email,))
    email_exist = c.fetchone()
    if email_exist:
        return "Email adressen finns redan"

    c.execute('''INSERT INTO Users (email, password) VALUES (?, ?)''',
              (email, password_hash))
    conn.commit()
    redirect("/")

@route("/login", method="GET")
def login():
    return template('views/login')

@route('/login', method='POST')
def do_login():
    email = getattr(request.forms,'email')
    password = getattr(request.forms,'password')

    conn = sqlite3.connect('pingo.db')
    c = conn.cursor()
    c.execute("SELECT email, password FROM Users WHERE email=?", (email,))
    user = c.fetchone()

    if not user:
        return "Invalid email or password"
    
    if user[1] != hashlib.sha256(password.encode()).hexdigest():
        return "Invalid email or password"

    redirect('/')



@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./views/static')


@route('/profile')
def profile():
    return template('views/profile')


@route('/start/<category>')
def start(category):
    conn = sqlite3.connect('pingo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT challenge_name FROM Challenges
                 WHERE category_id = (SELECT id FROM Categories WHERE category_name = ?)''', (category,))
    challenges = [row['challenge_name'] for row in c.fetchall()]

    conn.close()

    return template('views/start', data=challenges, category=category)

@route('/starting', method='POST')
def starting_game():
    category = get_category_from_database()

    hour = request.forms.get('hour')
    minute = request.forms.get('minute')
    second = request.forms.get('second')

    redirect('/bingo/{}?hour={}&minute={}&second={}'.format(category, hour, minute, second))


run(host='127.0.0.1', port=8080, reloader=True, debug=True)
