from flask import Flask, request, jsonify, render_template, redirect
import json
from datetime import datetime
import uuid
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

    new_task = request.get_json()  # Get JSON payload from the request
    new_id = str(uuid.uuid4())
    
    if not new_task.get('name') or not new_task.get('author'):
        return jsonify({'error': 'Missing task name or author'}), 400
    
    # Strip leading/trailing spaces from input fields
    name = new_task.get('name', '').strip()
    author = new_task.get('author', '').strip()

    # Check if name or author exceeds the allowed character limit
    if len(name) > MAX_LENGTH or len(author) > MAX_LENGTH:
        return jsonify({'error': 'Name or author too long'}), 400

    tasks = load_tasks()  # Load existing tasks from the JSON file
    
    new_task['task_date_create'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_task['uuid'] = new_id
    tasks[new_id] = new_task
    
    save_tasks(tasks)  # Write updated tasks back to the file
    # # return response
    return jsonify(new_id)



@app.route('/tasks/<uuid>', methods=['PUT'])
def update_task(uuid):
    tasks = load_tasks()
    if uuid not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    tasks[uuid]['name'] = data.get('name', tasks[uuid]['name'])    
    save_tasks(tasks)
    
    return jsonify({'message': 'Task updated'}), 200

@app.route('/tasks/<uuid>', methods=['DELETE'])
def delete_task(uuid):
    tasks = load_tasks()
    if uuid in tasks:
        del tasks[uuid]
        save_tasks(tasks)
        return jsonify({'message': 'Task deleted'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # Enable debug mode by default unless DEBUG env var is explicitly set to false
    debug = os.environ.get('DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug, port=port)
