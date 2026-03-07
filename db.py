import sqlite3
from flask import Flask, request, jsonify

def get_conn():
    conn = sqlite3.connect("new.db")
    conn.row_factory = sqlite3.Row
    return conn

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
    conn.commit()
    conn.close()

def basic_validation(name, number, email, address):
    if not name:
            return jsonify({"error": "name required"}), 400
    if not number:
            return jsonify({"error": "number required"}), 400
    if not email:
            return jsonify({"error": "email required"}), 400
    if not address:
            return jsonify({"error": "address required"}), 400
    if not isinstance(name, str):
        return jsonify({"error": "name must be strings"}), 400
    if not isinstance(number, int):
         return jsonify({"error": "number must be integer"}), 400
    if not isinstance(email, str) or not isinstance(address, str):
        return jsonify({"error": "email and address must be strings"}), 400