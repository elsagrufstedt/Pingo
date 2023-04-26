import sqlite3
import json

# Define a function to decode UTF-8 data
def utf8_decoder(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return str(data)

# Connect to the database
conn = sqlite3.connect('pingo.db')
c = conn.cursor()

# Create the Categories table
c.execute('''CREATE TABLE Categories (
                id INTEGER PRIMARY KEY,
                category_name TEXT NOT NULL
            )''')

# Create the Challenges table
c.execute('''CREATE TABLE Challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                challenge_name TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES Categories(id)
            )''')

# Load the JSON file
with open('views/static/categories.json', 'r') as f:
    data = json.load(f)

# Insert data into the Categories and Challenges tables
for category_data in data:
    category_id = category_data['id']
    category_name = category_data['category']
    c.execute('INSERT INTO Categories (id, category_name) VALUES (?, ?)', (category_id, category_name))

    for challenge_name in category_data['challenges']:
        c.execute('INSERT INTO Challenges (challenge_name, category_id) VALUES (?, ?)', (challenge_name, category_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
