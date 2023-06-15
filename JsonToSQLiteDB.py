import json
import sqlite3

conn = sqlite3.connect('issue_tracker.db')
cursor = conn.cursor()

# Creating the database schema
cursor.execute('''CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY,
                    type TEXT,
                    state TEXT,
                    title TEXT,
                    body TEXT,
                    user TEXT,
                    closed_at TEXT,
                    started_at TEXT,
                    repository TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS labels (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS issue_labels (
                    issue_id INTEGER,
                    label_id INTEGER,
                    FOREIGN KEY (issue_id) REFERENCES issues(id),
                    FOREIGN KEY (label_id) REFERENCES labels(id),
                    PRIMARY KEY (issue_id, label_id)
                )''')

# Loading the JSON data
with open('sample.json', 'r') as file:
    json_data = json.load(file)

# Inserting data into the tables
for issue in json_data:
    cursor.execute('''INSERT INTO issues (id, type, state, title, body, user, closed_at, started_at, repository)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (issue['id'], issue['type'], issue['state'], issue['title'], issue['body'], issue['user'],
                    issue['closed_at'], issue['started_at'], issue['repository']))

    for label in issue['labels']:
        cursor.execute('''INSERT INTO labels (id, name)
                          VALUES (?, ?)''',
                       (label['id'], label['name']))

        cursor.execute('''INSERT INTO issue_labels (issue_id, label_id)
                          VALUES (?, ?)''',
                       (issue['id'], label['id']))

conn.commit()
conn.close()
