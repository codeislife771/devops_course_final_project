from flask import Flask, request, jsonify, render_template, redirect
import json
from datetime import datetime
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

    
def load_tasks():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)


@app.route('/', methods=['GET'])
def redirect_to_tasks():
    return redirect('/tasks', code=302)

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "ok"}, 200

@app.route('/tasks', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

@app.route('/tasks', methods=['POST'])
def create_task():
    MAX_LENGTH = 100  # Maximum allowed length for task name and author

    data = request.get_json()  # Get JSON payload from the request

    # Strip leading/trailing spaces from input fields
    name = data.get('name', '').strip()
    author = data.get('author', '').strip()

    # Check if name or author is missing or contains only spaces
    if not name or not author:
        return jsonify({'error': 'Invalid or missing task name or author'}), 400

    # Check if name or author exceeds the allowed character limit
    if len(name) > MAX_LENGTH or len(author) > MAX_LENGTH:
        return jsonify({'error': 'Name or author too long'}), 400

    tasks = load_tasks()  # Load existing tasks from the JSON file

    # Check if a task with the same (stripped) name already exists
    if name in tasks:
        return jsonify({'error': 'Duplicate task name'}), 400

    # Save the new task with current creation date
    tasks[name] = {
        'author': author,
        'date_create': datetime.now().strftime('%Y-%m-%d')
    }

    save_tasks(tasks)  # Write updated tasks back to the file

    return jsonify({'message': 'Task created'}), 201  # Success response with HTTP 201


@app.route('/tasks/<name>', methods=['PUT'])
def update_task(name):
    tasks = load_tasks()
    if name not in tasks:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    tasks[name]['author'] = data.get('author', tasks[name]['author'])
    save_tasks(tasks)
    return jsonify({'message': 'Task updated'}), 200

@app.route('/tasks/<name>', methods=['DELETE'])
def delete_task(name):
    tasks = load_tasks()
    if name in tasks:
        del tasks[name]
        save_tasks(tasks)
        return jsonify({'message': 'Task deleted'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # Enable debug mode by default unless DEBUG env var is explicitly set to false
    debug = os.environ.get('DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug, port=port)
