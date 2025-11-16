from datetime import datetime
from flask import jsonify, request
import uuid
from my_app import app

users = {}
categories = {}
records = {}

@app.route('/healthcheck')
def healthcheck():
    response_data = {
        'status': 'OK',
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response_data), 200

@app.route('/')
def index():
    return "Hello, user! Check the /healthcheck endpoint."

@app.post('/user')
def create_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex
    user = {"id": user_id, "name": user_data["name"]}
    users[user_id] = user
    return jsonify(user), 201 

@app.get('/users')
def get_users():
    return jsonify(list(users.values()))

@app.get('/user/<user_id>')
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404 

@app.delete('/user/<user_id>')
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return "", 204 
    return jsonify({"error": "User not found"}), 404