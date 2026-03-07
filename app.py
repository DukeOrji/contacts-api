"""
This software was create dto showcase my technical skills, such as: 
error handling, authenticative authorization, sql usage, technical framework architechture
------
This software houses tables for a user and their contact info, such as:
phone number, email, address
"""

from flask import Flask, Blueprint, request, jsonify
from db import init_db

app = Flask(__name__)

from routes.sys import sys_bp
from routes.modify import modify_bp
app.register_blueprint(sys_bp)
app.register_blueprint(modify_bp)


@app.route("/")
def home():
    return "API is running", 200



if __name__ == "__main__":
    init_db()
    app.run(debug=True)