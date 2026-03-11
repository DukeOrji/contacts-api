
from flask import Flask, Blueprint, request, jsonify
from db import init_db

app = Flask(__name__) #initialize application server

from routes.sys import sys_bp
from routes.modify import modify_bp
app.register_blueprint(sys_bp)
app.register_blueprint(modify_bp)


@app.route("/")
def home():
    return "API is running", 200 #health check for server



if __name__ == "__main__":
    init_db()
    app.run(debug=True)