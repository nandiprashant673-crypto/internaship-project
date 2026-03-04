from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
# This line fixes the red error in your browser console
CORS(app)

# MySQL Connection - Make sure your password is correct here
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Prashant@2002",
    database="fullstack_db"
)

cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return "Backend Connected to MySQL Successfully!"

# 1. REGISTER API
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    email = data["email"]
    password = data["password"]

    try:
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, password)
        cursor.execute(query, values)
        db.commit()
        return jsonify({"message": "User Registered Successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 2. LOGIN API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    query = "SELECT id, name FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login Successful!", "user": user}), 200
    else:
        return jsonify({"message": "Invalid Credentials!"}), 401

# 3. ADD TASK API
@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.json
    user_id = data["user_id"]
    task = data["task"]

    query = "INSERT INTO tasks (user_id, task) VALUES (%s, %s)"
    cursor.execute(query, (user_id, task))
    db.commit()
    return jsonify({"message": "Task Added Successfully!"})

# 4. VIEW TASKS API
@app.route("/get-tasks/<int:user_id>", methods=["GET"])
def get_tasks(user_id):
    query = "SELECT * FROM tasks WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    return jsonify(tasks)

# 5. DELETE TASK API
@app.route("/delete-task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    query = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    db.commit()
    return jsonify({"message": "Task Deleted Successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
