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

@app.post('/category')
def create_category():
    category_data = request.get_json()
    category_id = uuid.uuid4().hex
    category = {"id": category_id, "name": category_data["name"]}
    categories[category_id] = category
    return jsonify(category), 201

@app.get('/category')
def get_categories():
    return jsonify(list(categories.values()))

@app.delete('/category/<category_id>')
def delete_category(category_id):
    if category_id in categories:
        del categories[category_id]
        return "", 204
    return jsonify({"error": "Category not found"}), 404

@app.post('/record')
def create_record():
    record_data = request.get_json()
    user_id = record_data.get('user_id')
    category_id = record_data.get('category_id')

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    if category_id not in categories:
        return jsonify({"error": "Category not found"}), 404

    record_id = uuid.uuid4().hex
    record = {
        "id": record_id,
        "user_id": user_id,
        "category_id": category_id,
        "created_at": datetime.now().isoformat(),
        "amount": record_data.get('amount')
    }
    records[record_id] = record
    return jsonify(record), 201

@app.get('/record/<record_id>')
def get_record(record_id):
    record = records.get(record_id)
    if record:
        return jsonify(record)
    return jsonify({"error": "Record not found"}), 404

@app.delete('/record/<record_id>')
def delete_record(record_id):
    if record_id in records:
        del records[record_id]
        return "", 204
    return jsonify({"error": "Record not found"}), 404

@app.get('/record')
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({"error": "At least one filter (user_id or category_id) is required"}), 400

    filtered_records = list(records.values())

    if user_id:
        filtered_records = [r for r in filtered_records if r['user_id'] == user_id]

    if category_id:
        filtered_records = [r for r in filtered_records if r['category_id'] == category_id]
    
    return jsonify(filtered_records)