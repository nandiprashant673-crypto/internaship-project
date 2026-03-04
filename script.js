// --- 1. REGISTER FUNCTION ---
async function register() {
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPass').value;

    const response = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "name": name, "email": email, "password": password })
    });

    const data = await response.json();
    alert(data.message);
}

// --- 2. LOGIN FUNCTION ---
async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPass').value;

    const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "email": email, "password": password })
    });

    const data = await response.json();

    if (response.status === 200) {
        alert("Welcome " + data.user.name + "!");
        localStorage.setItem('userId', data.user.id);
        window.location.href = "dashboard.html"; 
    } else {
        alert(data.message || "Invalid Credentials!");
    }
}

// --- 3. ADD TASK FUNCTION ---
async function addTask() {
    const userId = localStorage.getItem('userId');
    const task = document.getElementById('taskInput').value;

    if (!task) {
        alert("Please enter a task!");
        return;
    }

    await fetch('http://127.0.0.1:5000/add-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "user_id": userId, "task": task })
    });

    document.getElementById('taskInput').value = ''; 
    getTasks(); 
}

// --- 4. VIEW TASKS FUNCTION ---
async function getTasks() {
    const userId = localStorage.getItem('userId');
    const response = await fetch(`https://internaship-project.onrender.com/get-tasks/${userId}`);
    const tasks = await response.json();

    const taskList = document.getElementById('taskList');
    taskList.innerHTML = ''; 

    tasks.forEach(t => {
        const taskDiv = document.createElement('div');
        taskDiv.style = "display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #ddd; align-items: center;";
        taskDiv.innerHTML = `
            <span>${t.task}</span>
            <button onclick="deleteTask(${t.id})" style="width: 80px; background-color: #dc3545; color: white; border: none; padding: 5px; border-radius: 4px; cursor: pointer;">Delete</button>
        `;
        taskList.appendChild(taskDiv);
    });
}

// --- 5. DELETE TASK FUNCTION ---
async function deleteTask(taskId) {
    if (confirm("Are you sure you want to delete this task?")) {
        await fetch(`http://127.0.0.1:5000/delete-task/${taskId}`, { method: 'DELETE' });
        getTasks(); 
    }
}

// --- 6. LOGOUT FUNCTION ---
function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}