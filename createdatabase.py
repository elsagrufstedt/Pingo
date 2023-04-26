import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('pingo.db')
c = conn.cursor()

# Load the JSON file
with open('views/static/categories.json', 'r') as f:
    data = json.load(f)

# Insert data into the Categories table
category_id = data['id']
category_name = data['category']
c.execute('INSERT INTO Categories (id, category_name) VALUES (?, ?)', (category_id, category_name))

# Insert data into the Challenges table
for challenge_id, challenge_name in enumerate(data['challenges'], start=1):
    c.execute('INSERT INTO Challenges (id, challenge_name, category_id) VALUES (?, ?, ?)', (challenge_id, challenge_name, category_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
