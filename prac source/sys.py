from flask import Blueprint, request, jsonify
import sqlite3
from db import get_conn
from auth import require_api_key
sys_bp = Blueprint("sys", __name__) #create blueprint - easily register endpoints



#Insert sample data into rows
@sys_bp.route("/users", methods= ["POST"])  
#@require_api_key  
def insert_data():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    name = data.get("name")
    number = data.get("number")

    conn = get_conn() 
    cur = conn.cursor()

    #make sure the user is string (basic validation)
    if not name or not number:
            return jsonify({"error": "name and number required"}), 400
    if not isinstance(name, str) or not isinstance(number, str):
        return jsonify({"error": "name and number must be strings"}), 400
    
    try:
        cur.execute("INSERT INTO users (name) VALUES(?)", (name,))
        user_id = cur.lastrowid
        cur.execute("INSERT INTO contacts (number, user_id) VALUES(?, ?)", (number, user_id))
        conn.commit()

        return jsonify({
            "name": name,
            "number": number,
            "user_id": user_id
        }), 201 #resouce is created

    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500 #server error

#link user to contact
@sys_bp.route("/users/<int:user_id>/contacts", methods=["GET"])
def list_user_table(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    if user is None:
        conn.close()
        return jsonify({"Error": "user id was not found"}), 404

    cur.execute("""
    SELECT users.name, contacts.number
    FROM users
    JOIN contacts ON users.id = contacts.user_id
    WHERE users.id = ?
    """, (user_id,))

    rows = cur.fetchall()
    if not rows: #takes account of list beign empty []
        conn.close()
        return jsonify({"error": "Table is empty"}), 404

    conn.close()
    return jsonify([dict(r) for r in rows]), 200


#display the complete table
@sys_bp.route("/users/contacts/list", methods = ["GET"])
def list_all_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT users.name, contacts.number
    FROM users
    JOIN contacts ON users.id = contacts.user_id
    ORDER BY users.id ASC
    """)

    rows = cur.fetchall()
    if len(rows) == 0:
        return jsonify({"message": "empty table."}), 404
    conn.close()
    return jsonify([dict(r) for r in rows]), 200