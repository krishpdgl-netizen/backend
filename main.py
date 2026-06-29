<!DOCTYPE html>
<html lang="en">
<head>
        <link rel="icon" type="image/png" href="static/favicon.png">

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manager Dashboard | Panache</title>
    <script>
        const role = localStorage.getItem("userRole");
        if (!role) { window.location.href = "index.html"; }
        if (role !== "manager") { window.location.href = "index.html"; }
    </script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }

        body {
            display: flex;
            background: #f4f6f9;
        }

        /* SIDEBAR */
        .sidebar {
            width: 260px;
            height: 100vh;
            background: #111827;
            color: white;
            position: fixed;
            left: 0;
            top: 0;
            padding: 20px;
        }

        .logo {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 30px;
        }

        .menu a {
            display: block;
            color: white;
            text-decoration: none;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            transition: 0.3s;
        }

        .menu a:hover {
            background: #2563eb;
        }

        .menu details summary {
            color: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            cursor: pointer;
            list-style: none;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .menu details summary:hover {
            background: #2563eb;
        }

        .review-badge {
            background: #ef4444;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 99px;
            min-width: 20px;
            text-align: center;
            display: none;
        }

        .menu details a {
            padding-left: 24px;
        }

        /* MAIN */
        .main {
            margin-left: 260px;
            width: 100%;
            padding: 25px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .header h1 {
            color: #111827;
        }

        .profile {
            background: white;
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
        }

        /* CARDS */
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,.08);
        }

        .card h2 {
            color: #2563eb;
            margin-bottom: 10px;
        }

        /* SECTION */
        .section {
            background: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,.08);
        }

        .section h2 {
            margin-bottom: 15px;
        }

        /* BUTTONS */
        .assign-btn {
            background: #2563eb;
            color: white;
            border: none;
            padding: 14px 25px;
            border-radius: 10px;
            cursor: pointer;
        }

        .assign-btn:hover {
            background: #1d4ed8;
        }

        .edit-btn {
            background: #f59e0b;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
        }

        .edit-btn:hover {
            background: #d97706;
        }

        .delete-btn {
            background: #dc2626;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
        }

        .delete-btn:hover {
            background: #b91c1c;
        }

        .review-btn {
            background: #f59e0b;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
        }

        .review-btn:hover {
            background: #d97706;
        }

        .approve-btn {
            background: #16a34a;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
        }

        .approve-btn:hover {
            background: #15803d;
        }

        .logout-btn {
            background: #dc2626;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
        }

        .logout-btn:hover {
            background: #b91c1c;
        }

        /* TABLE */
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 12px;
            border-bottom: 1px solid #eee;
            text-align: left;
        }

        th {
            background: #f3f4f6;
        }

        /* MODAL */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal {
            background: white;
            border-radius: 15px;
            padding: 30px;
            width: 480px;
            max-width: 95%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }

        .modal h2 {
            margin-bottom: 20px;
            color: #111827;
        }

        .modal label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #374151;
            font-size: 14px;
        }

        .modal input, .modal select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 14px;
        }

        .modal input:focus, .modal select:focus {
            outline: none;
            border-color: #2563eb;
        }

        .modal-actions {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-top: 5px;
        }

        .btn-cancel {
            background: #e5e7eb;
            color: #374151;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }

        .btn-save {
            background: #2563eb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }

        .btn-save:hover { background: #1d4ed8; }

        /* FILTER BUTTONS */
        .filter-bar {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }

        .filter-btn {
            border: 1.5px solid #e5e7eb;
            background: white;
            color: #6b7280;
            padding: 6px 16px;
            border-radius: 99px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
        }

        .filter-btn:hover { border-color: #2563eb; color: #2563eb; }

        .filter-btn.active {
            background: #2563eb;
            border-color: #2563eb;
            color: white;
        }

        /* STATUS BADGES */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 99px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-assigned    { background: #dbeafe; color: #1d4ed8; }
        .badge-inprogress  { background: #fef9c3; color: #a16207; }
        .badge-review      { background: #ffedd5; color: #c2410c; }
        .badge-completed   { background: #dcfce7; color: #15803d; }

        /* TOAST */
        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #111827;
            color: white;
            padding: 14px 22px;
            border-radius: 10px;
            font-size: 14px;
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s;
            z-index: 9999;
        }

        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }

        /* RESPONSIVE */
        @media (max-width: 900px) {
            .sidebar { width: 200px; }
            .main { margin-left: 200px; }
        }

    .review-btn{

    background:#16a34a;
    color:white;
    border:none;
    padding:8px 14px;
    border-radius:8px;
    cursor:pointer;

}

.review-btn:hover{

    background:#15803d;

}

        /* REMINDER WIDGET + BELL */
        .reminder-widget {
            background: white; padding: 20px 22px; border-radius: 15px;
            margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,.08);
        }
        .reminder-widget-header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;
        }
        .reminder-widget-header h2 { font-size: 17px; color: #111827; }
        .reminder-widget-header a { font-size: 13px; color: #2563eb; text-decoration: none; font-weight: 600; }
        .reminder-list { display: flex; flex-direction: column; gap: 10px; }
        .reminder-item {
            display: flex; align-items: center; gap: 12px; padding: 10px 12px;
            border-radius: 10px; background: #f9fafb; border-left: 4px solid #d1d5db;
        }
        .reminder-item.crit  { border-left-color: #dc2626; background: #fef2f2; }
        .reminder-item.high  { border-left-color: #f97316; background: #fff7ed; }
        .reminder-item.med   { border-left-color: #f59e0b; background: #fffbeb; }
        .reminder-item.low   { border-left-color: #6b7280; }
        .reminder-dot { font-size: 16px; line-height:1; flex-shrink:0; }
        .reminder-item-body { flex: 1; min-width:0; }
        .reminder-item-title { font-weight: 600; color: #111827; font-size: 14px; }
        .reminder-item-sub { font-size: 12px; color: #6b7280; }
        .reminder-item-amt { font-size: 13px; font-weight: 700; color: #111827; white-space:nowrap; }

        .bell-wrap { position: relative; }
        .bell-btn {
            width: 42px; height: 42px; border-radius: 50%; background: white;
            border: 1px solid #e5e7eb; cursor: pointer; font-size: 18px;
            display: flex; align-items: center; justify-content: center; position: relative;
        }
        .bell-btn:hover { background: #f3f4f6; }
        .bell-count {
            position: absolute; top: -4px; right: -4px; background: #dc2626; color: white;
            font-size: 10px; font-weight: 700; border-radius: 99px; min-width: 17px; height: 17px;
            display: flex; align-items: center; justify-content: center; padding: 0 4px;
        }
        .bell-dropdown {
            display: none; position: absolute; top: 50px; right: 0; width: 340px;
            max-height: 420px; overflow-y: auto; background: white; border-radius: 12px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.18); z-index: 2000; padding: 10px;
        }
        .bell-dropdown.active { display: block; }
        .bell-dropdown-header { font-weight: 700; font-size: 13px; color: #111827; padding: 6px 8px 10px; border-bottom: 1px solid #f3f4f6; margin-bottom: 6px; }
        .bell-item { padding: 9px 8px; border-radius: 8px; font-size: 13px; }
        .bell-item:hover { background: #f9fafb; }
        .bell-item-title { font-weight: 600; color: #111827; }
        .bell-item-sub { font-size: 12px; color: #6b7280; margin-top:2px; }
        .bell-empty { text-align:center; padding: 30px 10px; color: #9ca3af; font-size: 13px; }

    </style>
</head>

<body>

<!-- SIDEBAR -->
<div class="sidebar">
    <div class="logo">Panache WMS</div>
    <div class="menu">
        <a href="manager-dashboard.html">Dashboard</a><active>
                
        </active>
        <a href="sales-dashboard.html">Sales Dashboard</a>
        <a href="team-members.html">Team Members</a>
        <a href="reports.html">Reports</a>
        <a href="settings.html">Settings</a>
        <a href="calendar.html">Calendar</a>
        <a href="employee-hub.html">Employee Hub</a>
        <a href="letterhead.html">Letter head manager</a>
        <a href="attendance.html">Attendance manager</a>
        <a href="reminder.html">Reminders</a>
    </div>
<!-- ── PERSONAL TO-DO ─────────────────────────────── -->
<div style="margin-top:auto;padding-top:20px;border-top:0.5px solid rgba(255,255,255,0.12);">
    <p style="font-size:11px;font-weight:500;color:rgba(255,255,255,0.4);letter-spacing:0.6px;text-transform:uppercase;margin-bottom:10px;">My notes</p>

    <div id="sidebarTodos" style="display:flex;flex-direction:column;gap:6px;max-height:200px;overflow-y:auto;"></div>

    <div style="display:flex;gap:6px;margin-top:10px;">
        <input id="sidebarTodoInput"
               placeholder="Add a task..."
               style="flex:1;background:rgba(255,255,255,0.08);border:0.5px solid rgba(255,255,255,0.15);border-radius:6px;padding:6px 8px;font-size:12px;color:#fff;outline:none;"
               onkeydown="if(event.key==='Enter')addSidebarTodo()" />
        <button onclick="addSidebarTodo()"
                style="width:28px;height:28px;border-radius:6px;background:#2563eb;border:none;color:#fff;font-size:20px;cursor:pointer;line-height:1;flex-shrink:0;">+</button>
    </div>
</div>
</div>
<script>
(function() {
    const KEY = "panache_todos";

    function load() {
        try { return JSON.parse(localStorage.getItem(KEY)) || []; }
        catch { return []; }
    }

    function save(todos) {
        localStorage.setItem(KEY, JSON.stringify(todos));
    }

    function render() {
        const todos = load();
        const box   = document.getElementById("sidebarTodos");
        box.innerHTML = "";

        todos.forEach((text, i) => {
            const row = document.createElement("div");
            row.style.cssText = "display:flex;align-items:center;gap:8px;font-size:12px;color:rgba(255,255,255,0.8);line-height:1.4;";
            row.innerHTML = `
                <div onclick="completeSidebarTodo(${i})"
                     title="Mark complete — will be removed"
                     style="width:16px;height:16px;border-radius:50%;border:1.5px solid rgba(255,255,255,0.3);flex-shrink:0;cursor:pointer;display:flex;align-items:center;justify-content:center;"></div>
                <span>${text}</span>`;
            box.appendChild(row);
        });
    }

    window.addSidebarTodo = function() {
        const inp  = document.getElementById("sidebarTodoInput");
        const text = inp.value.trim();
        if (!text) return;
        const todos = load();
        todos.push(text);
        save(todos);
        inp.value = "";
        render();
    };

    window.completeSidebarTodo = function(i) {
        const circle = document.getElementById("sidebarTodos")
                               .children[i]
                               .querySelector("div");
        circle.style.background    = "#22c55e";
        circle.style.borderColor   = "#22c55e";
        circle.innerHTML           = `<svg width="10" height="10" viewBox="0 0 10 10"><polyline points="1.5,5 4,7.5 8.5,2.5" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
        setTimeout(() => {
            const todos = load();
            todos.splice(i, 1);
            save(todos);
            render();
        }, 500);
    };

    render();
})();
</script>
<!-- MAIN -->
<div class="main">

    <!-- HEADER -->
    <div class="header">
        <h1>Manager Dashboard</h1>
        <div style="display:flex;align-items:center;gap:15px;">
            <div class="profile">
                <b id="profileName">Loading...</b><br>
                <span id="profileEmail"></span><br>
                <span id="profileId"></span>
            </div>
            <div class="bell-wrap" id="bellWrap">
                <button class="bell-btn" onclick="toggleBellDropdown()">🔔<span class="bell-count" id="bellCount" style="display:none;"></span></button>
                <div class="bell-dropdown" id="bellDropdown"></div>
            </div>
            <button class="logout-btn" onclick="logout()">Logout</button>
        </div>
    </div>

    <!-- CARDS -->
    <!-- REMINDER WIDGET -->
    <div class="reminder-widget">
        <div class="reminder-widget-header">
            <h2>🔔 Upcoming Reminders</h2>
            <a href="reminder.html">View All</a>
        </div>
        <div class="reminder-list" id="reminderWidgetList">
            <div style="color:#9ca3af;font-size:14px;">Loading reminders...</div>
        </div>
    </div>

    <div class="cards">
        <div class="card">
            <h2 id="teamCount">—</h2>
            <p>Team Members</p>
        </div>
        <div class="card">
            <h2 id="totalTasks">—</h2>
            <p>Total Tasks</p>
        </div>
        <div class="card">
            <h2 id="completedTasks">—</h2>
            <p>Completed Tasks</p>
        </div>
        <div class="card">
            <h2 id="teamProductivity">—</h2>
            <p>Team Productivity</p>
        </div>
    </div>

    <!-- TASK MANAGEMENT -->
    <div class="section">
        <h2>Task Management</h2>
        <br>
        <button class="assign-btn" onclick="window.location.href='create-task.html'">
            Assign New Task
        </button>
    </div>

    <!-- ASSIGNED TASKS -->
    <div class="section">
        <h2>Assigned Tasks</h2>
        <br>
        <div class="filter-bar">
            <button class="filter-btn active" onclick="filterTasks('All')">All</button>
            <button class="filter-btn" onclick="filterTasks('In Progress')">In Progress</button>
            <button class="filter-btn" onclick="filterTasks('Pending Review')">Pending Review</button>
            <button class="filter-btn" onclick="filterTasks('Completed')">Completed</button>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Task</th>
                    <th>Employee Name</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Due Date</th>
                    <th>Edit</th>
                    <th>Delete</th>
                </tr>
            </thead>
            <tbody id="taskTable"></tbody>
        </table>
    </div>

    <div class="section">
    <div class="section-header">
        <h2>Tasks Pending Review</h2>
    </div>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Task</th>
                <th>Employee</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Attachment</th>
                <th>Review</th>
            </tr>
        </thead>

        <tbody id="reviewTable">
            <tr>
                <td colspan="6" style="text-align:center;">
                    Loading tasks...
                </td>
            </tr>
        </tbody>
    </table>
</div>

    <!-- TEAM MEMBERS -->
    <!-- end .main -->

<!-- EDIT TASK MODAL -->
<div class="modal-overlay" id="editModal">
    <div class="modal">
        <h2>Edit Task</h2>
        <input type="hidden" id="editTaskId">

        <label>Title</label>
        <input type="text" id="editTitle">

        <label>Description</label>
        <input type="text" id="editDescription">

        <label>Assign To (Team Member)</label>
        <select id="editAssignedTo">
            <option value="">— Select team member —</option>
        </select>

        <label>Priority</label>
        <select id="editPriority">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
        </select>

        <label>Due Date</label>
        <input type="date" id="editDueDate">

        <div class="modal-actions">
            <button class="btn-cancel" onclick="closeEditModal()">Cancel</button>
            <button class="btn-save" onclick="saveEditTask()">Save Changes</button>
        </div>
    </div>
</div>

<!-- TOAST -->
<div class="toast" id="toast"></div>

<script>
    const BASE = "https://backend-production-53f3.up.railway.app";
const managerId =
localStorage.getItem("userId");
    // Profile
    document.getElementById("profileName").innerHTML = localStorage.getItem("userName");
    document.getElementById("profileEmail").innerHTML = localStorage.getItem("userEmail");
    document.getElementById("profileId").innerHTML = "Manager ID: " + localStorage.getItem("userId");

    function logout() {
        localStorage.clear();
        window.location.href = "index.html";
    }

    function showToast(msg) {
        const t = document.getElementById("toast");
        t.textContent = msg;
        t.classList.add("show");
        setTimeout(() => t.classList.remove("show"), 3000);
    }

    // ── STATS ────────────────────────────────────────────────
    async function loadStats() {
        try {
            const response = await fetch(`${BASE}/manager-dashboard-stats?manager_id=${managerId}`);
            const data = await response.json();

            document.getElementById("teamCount").innerHTML       = data.team_members;
            document.getElementById("totalTasks").innerHTML      = data.total_tasks;
            document.getElementById("completedTasks").innerHTML  = data.completed_tasks;
            document.getElementById("teamProductivity").innerHTML = data.productivity + "%";
        } catch (e) {
            console.error("loadStats error:", e);
        }
    }
    loadStats();
    // ── TEAM MEMBERS (manager's team only) ──────────────────
    let teamMembers = [];

    async function loadEmployees() {
        try {
            const res = await fetch(`${BASE}/team?manager_id=${managerId}`);
            teamMembers = await res.json();
            let html = "";
            teamMembers.forEach(emp => {
                html += `
                    <tr>
                        <td>${emp.id}</td>
                        <td>${emp.full_name}</td>
                        <td>${emp.email}</td>
                        <td>${emp.task_count}</td>
                    </tr>`;
            });
            document.getElementById("employeeTable").innerHTML = html || `<tr><td colspan="4" style="text-align:center;color:#9ca3af;padding:20px;">No team members found.</td></tr>`;
        } catch (e) {
            console.error("loadEmployees error:", e);
        }
    }

    // ── ALL TASKS ────────────────────────────────────────────
    let allTasks        = [];
    let activeFilter    = "All";

    function statusBadge(status) {
        const map = {
            "Assigned":       "badge-assigned",
            "In Progress":    "badge-inprogress",
            "Pending Review": "badge-review",
            "Completed":      "badge-completed"
        };
        return `<span class="badge ${map[status] || "badge-assigned"}">${status}</span>`;
    }

    function formatDate(raw) {
        if (!raw) return "—";
        const d = new Date(raw);
        if (isNaN(d)) return raw;
        return d.toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
    }

    function renderTasks() {
        const filtered = activeFilter === "All"
            ? allTasks
            : allTasks.filter(t => t.status === activeFilter);

        if (!filtered.length) {
            document.getElementById("taskTable").innerHTML =
                `<tr><td colspan="8" style="text-align:center;color:#9ca3af;padding:20px;">No tasks found.</td></tr>`;
            return;
        }

        document.getElementById("taskTable").innerHTML = filtered.map(task => `
            <tr>
                <td>${task.id}</td>
                <td><b>${task.title}</b></td>
                <td>${task.employee_name}</td>
                <td>${task.priority}</td>
                <td>${statusBadge(task.status)}</td>
                <td>${formatDate(task.due_date)}</td>
                <td><button class="edit-btn" onclick="openEditModal(${task.id})">Edit</button></td>
                <td><button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button></td>
            </tr>`).join("");
    }

    function filterTasks(status) {
        activeFilter = status;
        document.querySelectorAll(".filter-btn").forEach(btn => {
            btn.classList.toggle("active", btn.textContent.trim() === status);
        });
        renderTasks();
    }

    async function loadTasks() {
        try {
            const res   = await fetch(`${BASE}/manager-tasks?manager_id=${managerId}`);
            allTasks    = await res.json();
            renderTasks();
        } catch (e) {
            console.error("loadTasks error:", e);
        }
    }

    // ── DELETE TASK ──────────────────────────────────────────
    async function deleteTask(taskId) {
        if (!confirm("Are you sure you want to delete this task?")) return;
        try {
            const res = await fetch(`${BASE}/delete-task?task_id=${taskId}`, { method: "POST" });
            const data = await res.json();
            if (data.success) {
                showToast("Task deleted.");
                refreshAll();
            }
        } catch (e) {
            console.error("deleteTask error:", e);
        }
    }

    // ── EDIT MODAL ───────────────────────────────────────────
    async function openEditModal(taskId) {
        try {
            const res = await fetch(`${BASE}/task?task_id=${taskId}`);
            const task = await res.json();
            if (!task || task.success === false) { showToast("Could not load task."); return; }

            document.getElementById("editTaskId").value      = task.id;
            document.getElementById("editTitle").value       = task.title;
            document.getElementById("editDescription").value = task.description || "";
            document.getElementById("editPriority").value    = task.priority;
            document.getElementById("editDueDate").value     = task.due_date ? task.due_date.split("T")[0] : "";

            // Populate dropdown with team members only
            const sel = document.getElementById("editAssignedTo");
            sel.innerHTML = `<option value="">— Select team member —</option>`;
            (teamMembers.length ? teamMembers : await fetch(`${BASE}/team?manager_id=${managerId}`).then(r => r.json()))
                .forEach(emp => {
                    const opt = document.createElement("option");
                    opt.value = emp.id;
                    opt.textContent = `${emp.full_name} (ID: ${emp.id})`;
                    if (emp.id === task.assigned_to) opt.selected = true;
                    sel.appendChild(opt);
                });

            document.getElementById("editModal").classList.add("active");
        } catch (e) {
            console.error("openEditModal error:", e);
        }
    }

    function closeEditModal() {
        document.getElementById("editModal").classList.remove("active");
    }

    async function saveEditTask() {
        const taskId      = document.getElementById("editTaskId").value;
        const title       = document.getElementById("editTitle").value.trim();
        const description = document.getElementById("editDescription").value.trim();
        const assignedTo  = document.getElementById("editAssignedTo").value;
        const priority    = document.getElementById("editPriority").value;
        const dueDate     = document.getElementById("editDueDate").value;

        if (!title || !assignedTo || !dueDate) { showToast("Please fill in all required fields."); return; }

        try {
            const params = new URLSearchParams({ task_id: taskId, title, description, assigned_to: assignedTo, priority, due_date: dueDate });
            const res  = await fetch(`${BASE}/edit-task?${params}`, { method: "POST" });
            const data = await res.json();
            if (data.success) {
                showToast("Task updated successfully.");
                closeEditModal();
                refreshAll();
            }
        } catch (e) {
            console.error("saveEditTask error:", e);
        }
    }

    // ── REVIEW TASKS ─────────────────────────────────────────
    async function loadReviewTasks() {
        try {
            const res   = await fetch(`${BASE}/review-tasks?manager_id=${managerId}`);
            const tasks = await res.json();

            // Update sidebar badge
            const badge = document.getElementById("reviewBadge");
            if (tasks.length > 0) {
                badge.textContent = tasks.length;
                badge.style.display = "inline-block";
            } else {
                badge.style.display = "none";
            }

            if (!tasks.length) {
                document.getElementById("reviewTable").innerHTML =
                    `<tr><td colspan="7" style="color:#9ca3af;text-align:center;padding:20px;">No tasks pending review</td></tr>`;
                return;
            }

            document.getElementById("reviewTable").innerHTML = tasks.map(task => {
                const fileCell = task.file_url
                    ? `<a href="${BASE}${task.file_url}" target="_blank"
                          style="color:#2563eb;font-size:13px;font-weight:600;text-decoration:none;
                                 display:inline-flex;align-items:center;gap:4px;">
                           📎 ${task.file_name || "View File"}
                       </a>`
                    : `<span style="color:#9ca3af;font-size:12px;">No file</span>`;
                return `
                <tr>
                    <td>${task.id}</td>
                    <td><b>${task.title}</b></td>
                    <td>${task.employee_name || task.assigned_to}</td>
                    <td>${task.priority}</td>
                    <td>${statusBadge(task.status)}</td>
                    <td>${fileCell}</td>
                    <td>
                        <button class="review-btn" onclick="openEditModal(${task.id})">Review</button>
                        <button class="approve-btn" onclick="approveTask(${task.id})">Approve</button>
                        <button onclick="openRemarkModal(${task.id}, ${task.assigned_to}, '${(task.title||'').replace(/'/g,"\\'")}')"
                                style="background:#f59e0b;color:white;border:none;padding:6px 12px;
                                       border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;margin-left:4px;">
                            Send Correction
                        </button>
                    </td>
                </tr>`;
            }).join("");
        } catch (e) {
            console.error("loadReviewTasks error:", e);
        }
    }

    // ── APPROVE TASK ─────────────────────────────────────────
    async function approveTask(taskId) {
        if (!confirm("Approve this task as Completed?")) return;
        try {
            const res  = await fetch(`${BASE}/approve-task?task_id=${taskId}`, { method: "POST" });
            const data = await res.json();
            if (data.success) {
                showToast("Task approved and marked as Completed.");
                refreshAll();
            }
        } catch (e) {
            console.error("approveTask error:", e);
        }
    }

    // ── REFRESH ALL ──────────────────────────────────────────
    function refreshAll() {
        loadStats();
        loadTasks();
        loadEmployees();
        loadReviewTasks();
    }

    // Close modal if clicking outside
    document.getElementById("editModal").addEventListener("click", function(e) {
        if (e.target === this) closeEditModal();
    });

    // Init
    refreshAll();
</script>
<!-- ── SEND CORRECTION MODAL ────────────────────────────────── -->
<div id="remarkModal" style="display:none;position:fixed;inset:0;
    background:rgba(0,0,0,0.5);z-index:1000;align-items:center;justify-content:center;">
    <div style="background:white;border-radius:14px;padding:28px;width:480px;max-width:95vw;">
        <h2 style="font-size:17px;margin-bottom:6px;color:#111827;">Send Correction</h2>
        <p id="remarkTaskLabel" style="font-size:13px;color:#6b7280;margin-bottom:18px;"></p>
        <input type="hidden" id="remarkTaskId" />
        <input type="hidden" id="remarkEmployeeId" />

        <label style="font-size:12px;font-weight:600;color:#6b7280;text-transform:uppercase;
                      letter-spacing:0.4px;display:block;margin-bottom:6px;">
            Correction / Remark
        </label>
        <textarea id="remarkText" rows="4"
                  placeholder="Describe what needs to be corrected or improved..."
                  style="width:100%;padding:10px 12px;border:1.5px solid #e5e7eb;border-radius:8px;
                         font-size:14px;font-family:'Segoe UI',sans-serif;outline:none;
                         resize:vertical;margin-bottom:18px;"></textarea>

        <div style="display:flex;gap:10px;justify-content:flex-end;">
            <button onclick="closeRemarkModal()"
                    style="background:#e5e7eb;color:#374151;border:none;padding:10px 20px;
                           border-radius:8px;cursor:pointer;font-size:14px;">Cancel</button>
            <button onclick="submitRemark()"
                    style="background:#f59e0b;color:white;border:none;padding:10px 20px;
                           border-radius:8px;cursor:pointer;font-size:14px;font-weight:600;">
                    Send Correction
            </button>
        </div>
    </div>
</div>

<script>
function openRemarkModal(taskId, employeeId, taskTitle) {
    document.getElementById("remarkTaskId").value     = taskId;
    document.getElementById("remarkEmployeeId").value = employeeId;
    document.getElementById("remarkTaskLabel").textContent = `Task: ${taskTitle}`;
    document.getElementById("remarkText").value       = "";
    document.getElementById("remarkModal").style.display = "flex";
}

function closeRemarkModal() {
    document.getElementById("remarkModal").style.display = "none";
}

async function submitRemark() {
    const taskId     = document.getElementById("remarkTaskId").value;
    const employeeId = document.getElementById("remarkEmployeeId").value;
    const remark     = document.getElementById("remarkText").value.trim();

    if (!remark) { showToast("Please enter a correction remark."); return; }

    const res = await fetch(
        `${BASE}/send-remark?task_id=${taskId}&manager_id=${managerId}` +
        `&employee_id=${employeeId}&remark=${encodeURIComponent(remark)}`,
        { method: "POST" }
    ).then(r => r.json());

    if (res.success) {
        showToast("Correction sent. Task moved back to In Progress.");
        closeRemarkModal();
        refreshAll();
    } else {
        showToast("Failed to send correction.");
    }
}

document.getElementById("remarkModal").addEventListener("click", function(e) {
    if (e.target === this) closeRemarkModal();
});
</script>

<script>
(function() {
    const RBASE = "https://backend-production-53f3.up.railway.app";
    const ruid  = localStorage.getItem("userId");
    const rrole = localStorage.getItem("userRole") || "employee";
    if (!ruid) return;

    function priorityClass(p) {
        if (p === "Critical") return "crit";
        if (p === "High") return "high";
        if (p === "Medium") return "med";
        return "low";
    }
    function dot(p) {
        if (p === "Critical" || p === "High") return "🔴";
        if (p === "Medium") return "🟠";
        return "🟡";
    }
    function lineFor(days) {
        if (days < 0) return `Overdue by ${Math.abs(days)} day(s)`;
        if (days === 0) return "Due Today";
        if (days === 1) return "Due Tomorrow";
        return `Due in ${days} Days`;
    }

    async function loadWidgetAndBell() {
        let items = [];
        try {
            const res = await fetch(`${RBASE}/reminders/today?user_id=${ruid}&role=${rrole}`);
            items = await res.json();
        } catch (e) { items = []; }

        renderWidget(items);
        renderBell(items);
    }

    function renderWidget(items) {
        const list = document.getElementById("reminderWidgetList");
        if (!list) return;
        if (!items || items.length === 0) {
            list.innerHTML = `<div style="color:#9ca3af;font-size:14px;padding:6px 2px;">No reminders today.</div>`;
            return;
        }
        list.innerHTML = items.slice(0, 6).map(r => `
            <div class="reminder-item ${priorityClass(r.priority)}">
                <span class="reminder-dot">${dot(r.priority)}</span>
                <div class="reminder-item-body">
                    <div class="reminder-item-title">${r.title}</div>
                    <div class="reminder-item-sub">${r.category} • ${lineFor(r.days_remaining)}</div>
                </div>
                ${r.amount ? `<div class="reminder-item-amt">₹${Number(r.amount).toLocaleString("en-IN")}</div>` : ""}
            </div>
        `).join("");
    }

    function renderBell(items) {
        const countEl = document.getElementById("bellCount");
        const dropEl  = document.getElementById("bellDropdown");
        if (!countEl || !dropEl) return;

        if (!items || items.length === 0) {
            countEl.style.display = "none";
            dropEl.innerHTML = `<div class="bell-dropdown-header">Notifications</div><div class="bell-empty">No reminders today.</div>`;
            return;
        }
        countEl.style.display = "flex";
        countEl.innerText = items.length > 9 ? "9+" : items.length;

        dropEl.innerHTML = `<div class="bell-dropdown-header">Reminders & Notifications</div>` +
            items.map(r => `
                <div class="bell-item" onclick="window.location.href='reminder.html'">
                    <div class="bell-item-title">${dot(r.priority)} ${r.title}</div>
                    <div class="bell-item-sub">${r.category} • ${lineFor(r.days_remaining)}</div>
                </div>
            `).join("");
    }

    window.toggleBellDropdown = function() {
        document.getElementById("bellDropdown").classList.toggle("active");
    };
    document.addEventListener("click", function(e) {
        const wrap = document.getElementById("bellWrap");
        if (wrap && !wrap.contains(e.target)) {
            document.getElementById("bellDropdown").classList.remove("active");
        }
    });

    loadWidgetAndBell();
})();
</script>

</body>
</html>
