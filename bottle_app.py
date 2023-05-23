from bottle import run, route, template, TEMPLATE_PATH, static_file, request, redirect
from aiohttp import web
import socketio
import asyncio
import os
import sqlite3
import hashlib

sio = socketio.AsyncServer()
'''Skapar en ny async socket io server'''
app = web.Application()
'''Skapar en ny Aiohttp webb applikation'''
sio.attach(app)
'''Kopplar ihop socket.io servern till webb applikationen'''

base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'views')
TEMPLATE_PATH.insert(0, views_path)

'''Socket.io koden'''
async def index(request):
    with open("index.html") as f:
        return web.Response(text=f.read(), content_type="text/html")

@sio.on("message")
async def print_message(sid, message):
    print("Socket ID: ", sid)
    print(message)

app.router.add_get("/", index)

if __name__ == "__main__":
    web.run_app(app)

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

    return template('views/bingo', data=challenges, category=category)


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


run(host='127.0.0.1', port=8080, reloader=True, debug=True)
