from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# This is crucial for your Netlify frontend to talk to your Render backend
CORS(app)

# Temporary in-memory database (No MySQL needed for this demo)
# This allows your mentor to test the app immediately
users = [
    {"id": 1, "name": "Prashant", "email": "prashant@gmail.com", "password": "123"}
]
tasks = []

@app.route("/")
def home():
    return "Backend is Live and Running! Database is in-memory for demo."

# --- 1. REGISTER API ---
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }
    users.append(new_user)
    return jsonify({"message": "User Registered Successfully!"}), 201

# --- 2. LOGIN API ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    # Check if user exists in our temporary list
    user = next((u for u in users if u["email"] == data["email"] and u["password"] == data["password"]), None)
    
    if user:
        return jsonify({"message": "Login Successful!", "user": user}), 200
    return jsonify({"message": "Invalid Credentials!"}), 401

# --- 3. ADD TASK API ---
@app.route("/add-task", methods=["POST"])
def add_task():
    data = request.json
    new_task = {
        "id": len(tasks) + 1, 
        "user_id": int(data["user_id"]), 
        "task": data["task"]
    }
    tasks.append(new_task)
    return jsonify({"message": "Task Added Successfully!"})

# --- 4. VIEW TASKS API ---
@app.route("/get-tasks/<int:user_id>", methods=["GET"])
def get_tasks(user_id):
    # Filter tasks for the specific user
    user_tasks = [t for t in tasks if t["user_id"] == user_id]
    return jsonify(user_tasks)

# --- 5. DELETE TASK API ---
@app.route("/delete-task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task Deleted Successfully!"})

if __name__ == "__main__":
    app.run(debug=True)

