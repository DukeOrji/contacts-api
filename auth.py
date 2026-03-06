from flask import Flask, request, jsonify

API_KEY = "abc123"

def require_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401