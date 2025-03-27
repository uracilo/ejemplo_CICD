# 🚀 Flask API con Docker, MySQL y GitHub Actions

Este repositorio contiene una API Flask con un CRUD de tareas conectado a una base de datos MySQL, empaquetada en un contenedor Docker, y con integración continua (CI/CD) mediante GitHub Actions.

---

## 📌 Estructura del Proyecto

```
/flask-docker-app
│── .github/
│   └── workflows/
│       ├── ci.yml          # Construcción y Push a Docker Hub
│       └── cd.yml          # Pull y ejecución del contenedor
│── app.py                  # API Flask con CRUD
│── db.py                   # Conexión a MySQL
│── Dockerfile              # Construcción del contenedor
│── docker-compose.yml      # Definición de servicios Docker
│── README.md               # Documentación
```

---

## 🛠️ **Requisitos Previos**
1. **Cuenta en Docker Hub** (https://hub.docker.com/).
2. **Configurar Secrets en GitHub**:
   - `DOCKERHUB_USERNAME` → Tu usuario de Docker Hub.
   - `DOCKERHUB_TOKEN` → Token de acceso de Docker Hub (desde `https://hub.docker.com/settings/security`).

---

## 🚀 **1️⃣ API en Flask con CRUD (`app.py`)**

📄 **Archivo: `app.py`**
```python
from flask import Flask, request, jsonify
from db import init_db, get_db

app = Flask(__name__)
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
```

---

## 📂 **2️⃣ Base de Datos MySQL (`db.py`)**
📄 **Archivo: `db.py`**
```python
import sqlite3

def get_db():
    db = sqlite3.connect('tasks.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT)''')
    db.commit()
```

---

## 📦 **3️⃣ Dockerfile**
📄 **Archivo: `Dockerfile`**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY app.py db.py requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 🛠 **4️⃣ Docker Compose (`docker-compose.yml`)**
📄 **Archivo: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: tasks_db
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"

  app:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: "mysql://user:password@db/tasks_db"
    ports:
      - "5000:5000"
```

---

## ⚙️ **5️⃣ Workflow: Construcción y Push a Docker Hub**
📄 **Archivo: `.github/workflows/ci.yml`**
```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build Docker Image
        run: |
          docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/flask-mysql:latest .

      - name: Push Docker Image
        run: |
          docker push ${{ secrets.DOCKERHUB_USERNAME }}/flask-mysql:latest
```

---

## 🚀 **6️⃣ Workflow: Pull y Run desde Docker Hub**
📄 **Archivo: `.github/workflows/cd.yml`**
```yaml
name: Pull and Run Docker Image

on:
  workflow_run:
    workflows: ["Build and Push Docker Image"]
    types:
      - completed

jobs:
  pull-and-run:
    runs-on: ubuntu-latest

    steps:
      - name: Pull Docker Image
        run: |
          docker pull ${{ secrets.DOCKERHUB_USERNAME }}/flask-mysql:latest

      - name: Run Docker Container
        run: |
          docker-compose up -d
```

---


---

## 🛠 **Prueba Manual**


```bash
docker-compose up -d
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title": "Mi tarea", "description": "Descripción de la tarea"}'
curl http://localhost:5000/tasks
```
