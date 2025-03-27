from flask import Flask, request, jsonify
from db import init_db, get_db

app = Flask(__name__)


@app.route('/')
def home():
    print("Home route accessed")
    return "desde el nuevo commit!!!"

init_db()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return jsonify([dict(row) for row in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    db = get_db()
    data = request.json
    db.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (data['title'], data['description']))
    db.commit()
    return jsonify({'message': 'Task created'}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    db = get_db()
    data = request.json
    db.execute('UPDATE tasks SET title=?, description=? WHERE id=?', (data['title'], data['description'], id))
    db.commit()
    return jsonify({'message': 'Task updated'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id=?', (id,))
    db.commit()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)