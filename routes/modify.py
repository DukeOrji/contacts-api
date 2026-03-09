from flask import Blueprint, request, jsonify
from db import get_conn
from db import basic_validation as bv
from auth import require_api_key
modify_bp = Blueprint("modify", __name__)

#delete data implementations/empty the table for a specific user
@modify_bp.route("/users/<int:user_id>/contacts/del", methods=["DELETE"])
@require_api_key 
def del_user_table(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    if user is None:
        conn.close()
        return jsonify({"Error": "user id was not found"}), 404
    
    cur.execute("DELETE FROM contacts WHERE user_id=?", (user_id,))
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": "User Table has been cleared"}), 200

#delete data implementations/empty the table
@modify_bp.route("/users/contacts/del", methods = ["DELETE"])
@require_api_key 
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
@modify_bp.route("/users/<int:user_id>/contacts", methods = ["PUT"])
@require_api_key 
def update_list(user_id):
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    name = data.get("name")
    number = data.get("number")
    email = data.get("email")
    address = data.get("address")

    conn = get_conn()
    cur = conn.cursor()

    #make sure the user is string (basic validation)
    validation = bv(name, number, email, address)
    if validation:
        return validation
    
    cur.execute("UPDATE users SET name=? WHERE id=?", (name, user_id))
    cur.execute("""
    UPDATE contacts 
    SET number=?, email=?, address=?
    WHERE user_id=?
    """, (number, email, address, user_id))

    if cur.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    conn.commit()
    conn.close()
    return jsonify({"success": "User table updated"}), 200