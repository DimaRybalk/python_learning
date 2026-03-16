const API_ROOT = 'http://localhost:8000';
let currentUserId = localStorage.getItem('userId'); // Сразу проверяем память

const authSection = document.getElementById('auth-section');
const taskSection = document.getElementById('task-section');
const authMsg = document.getElementById('auth-msg');
const taskMsg = document.getElementById('task-msg');
const userInfo = document.getElementById('user-info');
const tasksList = document.getElementById('tasks-list');

const showMessage = (el, text, isError = false) => {
  if (!el) return;
  el.textContent = text;
  el.style.color = isError ? 'red' : 'green';
  setTimeout(() => { el.textContent = ''; }, 3000);
};

// Функция входа: сохраняем данные "намертво" в браузер
const setUser = (userId, email) => {
  currentUserId = userId;
  localStorage.setItem('userId', userId);
  localStorage.setItem('userEmail', email);

  authSection.classList.add('hidden');
  taskSection.classList.remove('hidden');
  userInfo.textContent = `Logged in as ${email} (ID ${userId})`;
  loadTasks();
};

const doApi = async (url, opts = {}) => {
  const res = await fetch(url, opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Server error');
  }
  return res.json();
};

const registerUser = async (e) => {
  e.preventDefault();
  const email = document.getElementById('reg-email').value.trim();
  const password = document.getElementById('reg-password').value;
  try {
    await doApi(`${API_ROOT}/registration`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    showMessage(authMsg, 'Registered! Now login.');
  } catch (e) {
    showMessage(authMsg, `Error: ${e.message}`, true);
  }
};

const loginUser = async (e) => {
  e.preventDefault();
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  try {
    const user = await doApi(`${API_ROOT}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    setUser(user.id, user.email);
  } catch (e) {
    showMessage(authMsg, `Login failed`, true);
  }
};

const loadTasks = async () => {
  if (!currentUserId) return;
  tasksList.innerHTML = 'Loading tasks...';
  try {
    const tasks = await doApi(`${API_ROOT}/tasks?user_id=${currentUserId}`);
    tasksList.innerHTML = '';
    if (!tasks.length) { tasksList.textContent = 'No tasks yet.'; return; }

    tasks.forEach((task) => {
      const card = document.createElement('div');
      card.className = `task-card ${task.is_complete ? 'completed' : ''}`;
      card.innerHTML = `
        <h3>${task.name}</h3>
        <p>${task.description || ''}</p>
        <div class="task-actions">
          <button onclick="toggleTask(${task.id})">${task.is_complete ? 'Unmark' : 'Done'}</button>
          <button onclick="deleteTask(${task.id})">Delete</button>
        </div>
      `;
      tasksList.appendChild(card);
    });
  } catch (e) {
    console.error(e);
  }
};

const createTask = async (e) => {
  e.preventDefault();
  const name = document.getElementById('task-name').value.trim();
  const description = document.getElementById('task-desc').value.trim();
  if (!name) return;

  try {
    await doApi(`${API_ROOT}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description, user_id: currentUserId })
    });
    document.getElementById('task-name').value = '';
    document.getElementById('task-desc').value = '';
    loadTasks();
  } catch (e) {
    showMessage(taskMsg, 'Error creating task', true);
  }
};

// Вынес функции в глобальную область, чтобы onclick в HTML их видел
window.toggleTask = async (taskId) => {
  await doApi(`${API_ROOT}/tasks/${taskId}/toggle?user_id=${currentUserId}`, { method: 'PATCH' });
  loadTasks();
};

window.deleteTask = async (taskId) => {
  if (confirm('Delete?')) {
    await doApi(`${API_ROOT}/tasks/${taskId}?user_id=${currentUserId}`, { method: 'DELETE' });
    loadTasks();
  }
};

const logout = () => {
  localStorage.clear();
  location.reload(); // Самый надежный способ очистить всё — перезагрузить страницу
};

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-register').onclick = registerUser;
  document.getElementById('btn-login').onclick = loginUser;
  document.getElementById('btn-add-task').onclick = createTask;
  document.getElementById('btn-logout').onclick = logout;

  // Автоматический вход при загрузке
  const savedEmail = localStorage.getItem('userEmail');
  if (currentUserId && savedEmail) {
    setUser(currentUserId, savedEmail);
  }
});