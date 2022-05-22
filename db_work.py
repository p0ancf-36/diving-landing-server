import sqlite3

connection = sqlite3.connect("database.sqlite3")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	surname TEXT,
	fname TEXT,
	sname TEXT,
	phone TEXT,
	email TEXT
)
""")

connection.commit()