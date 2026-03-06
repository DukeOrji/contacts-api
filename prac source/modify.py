from flask import requests, jsonify
from db import get_conn

#delete data implementations/empty the table for a specific user
@app.route("/users/<int:user_id>/contacts/del", methods=["DELETE"])
def del_user_table(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    if user is None:
        conn.close()
        return jsonify({"Error": "user id was not found"}), 404
    
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    cur.execute("DELETE FROM contacts WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": "User Table has been cleared"}), 200

#delete data implementations/empty the table
@app.route("/users/contacts/del", methods = ["DELETE"])
def delete_table():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM contacts")
    cur.execute("DELETE FROM sqlite_sequence WHERE name = 'users'") #allows the user_id to begin from 0
    cur.execute("DELETE FROM sqlite_sequence WHERE name = 'contacts'")
    conn.commit()
    
    conn.close()
    return jsonify({"success": "Table has been cleared"}), 200


#upadate implementations per user
@app.route("/users/<int:user_id>/contacts", methods = ["PUT"])
def update_list(user_id):
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
    
    cur.execute("UPDATE users SET name=? WHERE id=?", (name, user_id))
    cur.execute("UPDATE contacts SET number=? WHERE user_id=?", (number, user_id))
    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    conn.commit()
    conn.close()
    return jsonify({"success": "workout updated"}), 200