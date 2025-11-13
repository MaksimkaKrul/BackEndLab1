from datetime import datetime
from flask import jsonify
from my_app import app

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