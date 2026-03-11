import sqlite3
from flask import Flask, request, jsonify

def get_conn():
    conn = sqlite3.connect("new.db")
    conn.row_factory = sqlite3.Row
    return conn

#initially clear the database - for testing purposes
def clear_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts")
    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM sqlite_sequence WHERE name= 'users'")
    cur.execute("DELETE FROM sqlite_sequence WHERE name= 'contacts'")

    conn.commit()
    conn.close()

#create tables to store data
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # Contacts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        address TEXT NOT NULL,
        email TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    #clear_db()
    conn.commit()
    conn.close()

#input validation function - avoids redundancy
def basic_validation(name, number, email, address):
    if not all([name, number, email, address]):
        return jsonify({"error": "All fields are required"}), 400
    if not isinstance(name, str) or not isinstance(number, str):
        return jsonify({"error": "name and number must be strings"}), 400
    if not isinstance(email, str) or not isinstance(address, str):
        return jsonify({"error": "email and address must be strings"}), 400