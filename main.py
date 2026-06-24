from fastapi import FastAPI, UploadFile, File as FastAPIFile
from sqlalchemy import create_engine
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional 
from excel_helper import (
    add_projection,
    get_sales,
    update_achieved,
    get_all_weeks,
    get_sales_for_employees,
    admin_update_projection,
    raise_change_request,
    get_change_requests,
    resolve_change_request,
    current_week,
    FILE_NAME
)
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel
from typing import List
from sqlalchemy import text


class MeetingRequest(BaseModel):
    title: str
    description: str = ""
    meeting_date: str
    start_slot: int
    end_slot: int
    organizer_id: int
    location: str = ""
    attendees: List[int]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATABASE_URL = "postgresql://postgres:OJKDsedhwgqyuvTubYNEJssZeJkRUgiS@thomas.proxy.rlwy.net:22127/railway"

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode":"require"}
)

@app.get("/")
def home():
    return {"message":"Panache API Running"}

@app.post("/create-user")
def create_user():

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO users
            (full_name,email,password,role)
            VALUES
            (
                'Admin User',
                'admin@panache.com',
                'admin123',
                'admin'
            )
            """)
        )

        conn.commit()

    return {"message":"User Created"}


@app.post("/login")
def login(email: str, password: str):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM users
                WHERE email=:email
                AND password=:password
            """),
            {
                "email": email,
                "password": password
            }
        )

        user = result.fetchone()

    if user:
        return {
    "success": True,
    "id": user.id,
    "name": user.full_name,
    "email": user.email,
    "role": user.role
     
    }

    return {
        "success": False
    }


@app.post("/register")
def register_user(
    fullname: str,
    email: str,
    password: str,
    role: str
):

    with engine.connect() as conn:

        existing = conn.execute(
            text("""
                SELECT id
                FROM users
                WHERE full_name = :full_name
            """),
            {
                "full_name": fullname
            }
        ).fetchone()

        if existing:
            return {
                "success": False,
                "message": "Username already exists"
            }

        conn.execute(
            text("""
                INSERT INTO users
                (full_name,email,password,role)
                VALUES
                (:full_name,:email,:password,:role)
            """),
            {
                "full_name": fullname,
                "email": email,
                "password": password,
                "role": role
            }
        )

        conn.commit()

    return {
        "success": True,
        "message": "User created"
    }

@app.get("/profile")
def get_profile(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM users
                WHERE id = :id
            """),
            {"id": user_id}
        )

        user = result.fetchone()

    if not user:
        return {"success": False}

    return {
        "success": True,
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "role": user.role
    }


@app.get("/my-tasks")
def my_tasks(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM tasks
                WHERE assigned_to = :user_id
                AND status != 'Completed'
            """),
            {"user_id": user_id}
        )

        tasks = [
            dict(row._mapping)
            for row in result
        ]

    return tasks

@app.get("/user")
def get_user(email: str):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT full_name,
                       email,
                       role
                FROM users
                WHERE email = :email
            """),
            {
                "email": email
            }
        )

        user = result.fetchone()

    if not user:
        return {
            "success": False
        }

    return {
        "success": True,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role
    }

@app.post("/create-task")
def create_task(
    title: str,
    description: str,
    assigned_to: int,
    assigned_by: int,
    priority: str,
    status: str,
    due_date: str
):

    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO tasks
                (
                    title,
                    description,
                    assigned_to,
                    assigned_by,
                    priority,
                    status,
                    due_date
                )
                VALUES
                (
                    :title,
                    :description,
                    :assigned_to,
                    :assigned_by,
                    :priority,
                    :status,
                    :due_date
                )
            """),
            {
                "title": title,
                "description": description,
                "assigned_to": assigned_to,
                "assigned_by": assigned_by,
                "priority": priority,
                "status": status,
                "due_date": due_date
            }
        )

        conn.commit()

    return {
        "success": True,
        "message": "Task created"
    }

@app.get("/my-tasks")
def my_tasks(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM tasks
                WHERE assigned_to = :user_id
                AND status != 'Completed'
                ORDER BY created_at DESC
            """),
            {
                "user_id": user_id
            }
        )

        tasks = [
            dict(row._mapping)
            for row in result
        ]

    return tasks

@app.get("/all-tasks")
def all_tasks():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM tasks
                ORDER BY created_at DESC
            """)
        )

        tasks = [
            dict(row._mapping)
            for row in result
        ]

    return tasks

@app.put("/update-task-status")
def update_task_status(
    task_id: int,
    status: str
):

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE tasks
                SET status = :status
                WHERE id = :task_id
            """),
            {
                "status": status,
                "task_id": task_id
            }
        )

        conn.commit()

    return {
        "success": True
    }


@app.get("/dashboard-stats")
def dashboard_stats():

    with engine.connect() as conn:

        total_users = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM users
            """)
        ).scalar()

        total_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
            """)
        ).scalar()

        pending_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE Lower(status) = 'pending'
            """)
        ).scalar()

        completed_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE LOWER(status) = 'complete'
            """)
        ).scalar()

    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks
    }

@app.post("/complete-task")
def complete_task(task_id:int):

    with engine.connect() as conn:

        task = conn.execute(
            text("""
                SELECT *
                FROM tasks
                WHERE id=:id
            """),
            {"id":task_id}
        ).fetchone()

        conn.execute(
            text("""
                UPDATE tasks
                SET status='Completed'
                WHERE id=:id
            """),
            {"id":task_id}
        )

        conn.execute(
    text("""
        INSERT INTO task_history
        (
            task_id,
            employee_id,
            task_title,
            submitted_at
        )
        VALUES
        (
            :task_id,
            :employee_id,
            :task_title,
            :submitted_at
        )
    """),
    {
        "task_id": task.id,
        "employee_id": task.assigned_to,
        "task_title": task.title,
        "submitted_at": datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).isoformat()
    }
)
        conn.commit()

    return {"success":True}

@app.get("/history")
def history(user_id:int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM task_history
                WHERE employee_id=:id
                ORDER BY submitted_at DESC
            """),
            {"id":user_id}
        )

        history = [
            dict(row._mapping)
            for row in result
        ]

    return history


@app.get("/productivity-score")
def productivity_score(user_id:int):

    with engine.connect() as conn:

        total = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to=:id
            """),
            {"id":user_id}
        ).scalar()

        completed = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to=:id
                AND status='Completed'
            """),
            {"id":user_id}
        ).scalar()

    score = 0

    if total > 0:
        score = round((completed/total)*100)

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "score": score
    }

@app.get("/employees")
def get_employees():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                id,
                full_name,
                email,
                role
                FROM users
                WHERE role='employee'
            """)
        )

        employees = [
            dict(row._mapping)
            for row in result
        ]

    return employees

@app.get("/all-tasks")
def get_all_tasks():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM tasks
                ORDER BY id DESC
            """)
        )

        tasks = [
            dict(row._mapping)
            for row in result
        ]

    return tasks



@app.get("/employee-performance")
def employee_performance():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
            u.id,
            u.full_name,

            COUNT(t.id) as assigned,

            COUNT(
                CASE
                WHEN t.status='Completed'
                THEN 1
                END
            ) as completed

            FROM users u

            LEFT JOIN tasks t
            ON u.id=t.assigned_to

            WHERE u.role='employee'

            GROUP BY u.id,u.full_name
            """)
        )

        data=[]

        for row in result:

            assigned=row.assigned
            completed=row.completed

            score=0

            if assigned>0:
                score=round(
                    completed/assigned*100
                )

            data.append({
                "id":row.id,
                "name":row.full_name,
                "assigned":assigned,
                "completed":completed,
                "score":score
            })

    return data

@app.post("/delete-task")
def delete_task(task_id:int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE
                FROM tasks
                WHERE id=:id
            """),
            {"id":task_id}
        )

        conn.commit()

    return {
        "success":True
    }

@app.get("/employee-performance")
def employee_performance():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
            u.id,
            u.full_name,

            COUNT(t.id) AS assigned,

            COUNT(
                CASE
                WHEN t.status='Completed'
                THEN 1
                END
            ) AS completed

            FROM users u

            LEFT JOIN tasks t
            ON u.id=t.assigned_to

            WHERE u.role='employee'

            GROUP BY u.id,u.full_name
            """)
        )

        data=[]

        for row in result:

            assigned=row.assigned
            completed=row.completed

            score=0

            if assigned>0:
                score=round((completed/assigned)*100)

            data.append({
                "id":row.id,
                "name":row.full_name,
                "assigned":assigned,
                "completed":completed,
                "score":score
            })

    return data
@app.post("/edit-task")
def edit_task(
    task_id:int,
    title:str,
    description:str,
    assigned_to:int,
    priority:str,
    due_date:str
):

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE tasks
                SET
                    title=:title,
                    description=:description,
                    assigned_to=:assigned_to,
                    priority=:priority,
                    due_date=:due_date
                WHERE id=:task_id
            """),
            {
                "task_id": task_id,
                "title": title,
                "description": description,
                "assigned_to": assigned_to,
                "priority": priority,
                "due_date": due_date
            }
        )

        conn.commit()

    return {
        "success": True
    }

@app.get("/task")
def get_task(task_id:int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM tasks
                WHERE id=:id
            """),
            {"id":task_id}
        )

        task = result.fetchone()

    if not task:
        return {"success":False}

    return dict(task._mapping)

@app.get("/recent-activity")
def recent_activity():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                task_id,
                employee_id,
                task_title,
                completed_at
                FROM task_history
                ORDER BY completed_at DESC
                LIMIT 20
            """)
        )

        activity = [
            dict(row._mapping)
            for row in result
        ]

    return activity

@app.get("/dashboard-summary")
def dashboard_summary():

    with engine.connect() as conn:

        employees = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM users
                WHERE role='employee'
            """)
        ).scalar()

        tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
            """)
        ).scalar()

        completed = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE status='Completed'
            """)
        ).scalar()

    productivity = 0

    if tasks > 0:
        productivity = round(completed/tasks*100)

    return {
        "employees": employees,
        "tasks": tasks,
        "completed": completed,
        "productivity": productivity
    }

@app.get("/search-employee")
def search_employee(name:str):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                id,
                full_name,
                email
                FROM users
                WHERE full_name ILIKE :name
            """),
            {
                "name":f"%{name}%"
            }
        )

        employees = [
            dict(row._mapping)
            for row in result
        ]

    return employees

@app.get("/employee-details")
def employee_details(user_id:int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                id,
                full_name,
                email,
                role
                FROM users
                WHERE id=:id
            """),
            {"id":user_id}
        )

        employee = result.fetchone()

    if not employee:
        return {"success":False}

    return dict(employee._mapping)

@app.post("/approve-task")
def approve_task(task_id:int):

    with engine.connect() as conn:

        # Fetch task details before updating so we can log to history
        task = conn.execute(
            text("""
                SELECT *
                FROM tasks
                WHERE id=:id
            """),
            {"id":task_id}
        ).fetchone()

        conn.execute(
            text("""
                UPDATE tasks
                SET status='Completed'
                WHERE id=:id
            """),
            {"id":task_id}
        )

        # Insert into task_history so the employee's History page is populated
        if task:
            conn.execute(
                text("""
                    INSERT INTO task_history
                    (task_id, employee_id, task_title, submitted_at)
                    VALUES
                    (:task_id, :employee_id, :task_title, :submitted_at)
                """),
                {
                    "task_id":      task.id,
                    "employee_id":  task.assigned_to,
                    "task_title":   task.title,
                    "submitted_at": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
                }
            )

        conn.commit()

    return {"success":True}


@app.get("/review-tasks")
def review_tasks(manager_id:int):

    with engine.connect() as conn:

        rows = conn.execute(
            text("""
            SELECT *
            FROM tasks

            WHERE assigned_to IN(

                SELECT employee_id
                FROM team_members
                WHERE manager_id=:manager_id

            )

            AND LOWER(status)='pending review'
            """),
            {"manager_id":manager_id}
        ).fetchall()

    return [dict(row._mapping) for row in rows]


@app.post("/team/remove")
def remove_team_member(manager_id:int,
                       employee_id:int):

    print("manager =", manager_id)
    print("employee =", employee_id)

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                DELETE
                FROM team_members
                WHERE manager_id=:manager_id
                AND employee_id=:employee_id
            """),
            {
                "manager_id":manager_id,
                "employee_id":employee_id
            }
        )

        conn.commit()

    print("rows deleted =", result.rowcount)

    return {"success":True}

@app.get("/team")
def get_team(manager_id:int):

    with engine.connect() as conn:

        data = conn.execute(
            text("""
                SELECT
                    users.id,
                    users.full_name,
                    users.email,

                    COUNT(
                        CASE
                        WHEN LOWER(tasks.status) != 'completed'
                        THEN tasks.id
                        END
                    ) AS task_count

                FROM team_members

                JOIN users
                ON team_members.employee_id = users.id

                LEFT JOIN tasks
                ON tasks.assigned_to = users.id

                WHERE team_members.manager_id = :manager_id

                GROUP BY
                    users.id,
                    users.full_name,
                    users.email

                ORDER BY users.full_name
            """),
            {
                "manager_id":manager_id
            }
        ).fetchall()

    result = []

    for row in data:

        result.append({

            "id":row.id,

            "full_name":row.full_name,

            "email":row.email,

            "task_count":row.task_count

        })

    return result

@app.get("/manager-dashboard-stats")
def manager_dashboard_stats(manager_id:int):

    with engine.connect() as conn:

        # Team members
        team_members = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM team_members
                WHERE manager_id=:manager_id
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Total tasks assigned to team
        total_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to IN(
                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id
                )
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Completed tasks
        completed_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to IN(
                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id
                )
                AND LOWER(status)='completed'
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Pending tasks (not completed)
        pending_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to IN(
                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id
                )
                AND LOWER(status)!='completed'
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Tasks pending review
        review_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to IN(
                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id
                )
                AND LOWER(status)='pending review'
            """),
            {"manager_id":manager_id}
        ).scalar()

    # Productivity = completed / total * 100
    productivity = 0
    if total_tasks and total_tasks > 0:
        productivity = round(completed_tasks * 100 / total_tasks)

    return {
        "team_members":   team_members   or 0,
        "total_tasks":    total_tasks    or 0,
        "completed_tasks": completed_tasks or 0,
        "pending_tasks":  pending_tasks  or 0,
        "review_tasks":   review_tasks   or 0,
        "productivity":   productivity
    }

@app.get("/manager-tasks")
def manager_tasks(manager_id:int):

    with engine.connect() as conn:

        rows = conn.execute(
            text("""
                SELECT
                    tasks.id,
                    tasks.title,
                    users.full_name AS employee_name,
                    tasks.assigned_to,
                    tasks.priority,
                    tasks.status,
                    tasks.due_date

                FROM tasks

                JOIN users
                ON tasks.assigned_to = users.id

                WHERE tasks.assigned_to IN (

                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id

                )

                ORDER BY tasks.id DESC
            """),
            {"manager_id": manager_id}
        ).fetchall()

    return [dict(row._mapping) for row in rows]

@app.post("/team/add")
def add_team_member(manager_id:int, employee_id:int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO team_members(manager_id, employee_id)
                VALUES(:manager_id, :employee_id)
            """),
            {
                "manager_id":manager_id,
                "employee_id":employee_id
            }
        )

        conn.commit()

    return {
        "success":True
    }

@app.get("/manager-report")
def manager_report(manager_id:int):

    with engine.connect() as conn:

        # Team members
        team_members = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM team_members
                WHERE manager_id=:manager_id
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Assigned tasks
        assigned_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to IN(

                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id

                )
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Completed tasks
        completed_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to IN(

                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id

                )

                AND LOWER(status)='completed'
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Pending tasks
        pending_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE assigned_to IN(

                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id

                )

                AND LOWER(status)!='completed'
            """),
            {"manager_id":manager_id}
        ).scalar()

        # Completion rate
        if assigned_tasks == 0:
            completion_rate = 0
        else:
            completion_rate = round(
                completed_tasks * 100 / assigned_tasks
            )

        # Top performer
        top_performer_row = conn.execute(
            text("""
                SELECT
                    users.full_name,
                    COUNT(tasks.id) AS completed_count

                FROM users

                JOIN tasks
                ON users.id = tasks.assigned_to

                WHERE users.id IN(

                    SELECT employee_id
                    FROM team_members
                    WHERE manager_id=:manager_id

                )

                AND LOWER(tasks.status)='completed'

                GROUP BY users.full_name

                ORDER BY completed_count DESC

                LIMIT 1
            """),
            {"manager_id":manager_id}
        ).fetchone()

        top_performer = (
            top_performer_row.full_name
            if top_performer_row
            else "N/A"
        )

    return {

        "team_members": team_members or 0,

        "assigned_tasks": assigned_tasks or 0,

        "completed_tasks": completed_tasks or 0,

        "pending_tasks": pending_tasks or 0,

        "completion_rate": completion_rate,

        "top_performer": top_performer

    }
@app.post("/delete-user")
def delete_user(user_id: int):

    with engine.connect() as conn:

        # Delete tasks assigned to employee
        conn.execute(
            text("""
                DELETE FROM tasks
                WHERE assigned_to=:user_id
            """),
            {"user_id": user_id}
        )

        # Remove employee from teams
        conn.execute(
            text("""
                DELETE FROM team_members
                WHERE employee_id=:user_id
            """),
            {"user_id": user_id}
        )

        # Delete the user
        conn.execute(
            text("""
                DELETE FROM users
                WHERE id=:user_id
            """),
            {"user_id": user_id}
        )

        conn.commit()

    return {
        "success": True,
        "message": "User deleted successfully"
    }
@app.get("/managers")
def get_managers():

    with engine.connect() as conn:

        rows = conn.execute(
            text("""
                SELECT
                    id,
                    full_name,
                    email,
                    role
                FROM users
                WHERE LOWER(role)='manager'
                ORDER BY id
            """)
        ).fetchall()

    return [dict(row._mapping) for row in rows]


# ── UPDATE PROFILE ───────────────────────────────────────────────
@app.post("/update-profile")
def update_profile(user_id: int, full_name: str, email: str):
    with engine.connect() as conn:
 
        # Check email not taken by someone else
        existing = conn.execute(
            text("SELECT id FROM users WHERE email=:email AND id != :user_id"),
            {"email": email, "user_id": user_id}
        ).fetchone()
 
        if existing:
            return {"success": False, "message": "Email already in use by another account"}
 
        conn.execute(
            text("""
                UPDATE users
                SET full_name = :full_name, email = :email
                WHERE id = :user_id
            """),
            {"full_name": full_name, "email": email, "user_id": user_id}
        )
        conn.commit()
 
    return {"success": True, "message": "Profile updated"}
 
 
# ── CHANGE PASSWORD ──────────────────────────────────────────────
@app.post("/change-password")
def change_password(user_id: int, current_password: str, new_password: str):
    with engine.connect() as conn:
 
        # Verify current password
        user = conn.execute(
            text("SELECT id FROM users WHERE id=:user_id AND password=:password"),
            {"user_id": user_id, "password": current_password}
        ).fetchone()
 
        if not user:
            return {"success": False, "message": "Current password is incorrect"}
 
        if len(new_password) < 6:
            return {"success": False, "message": "New password must be at least 6 characters"}
 
        conn.execute(
            text("UPDATE users SET password=:password WHERE id=:user_id"),
            {"password": new_password, "user_id": user_id}
        )
        conn.commit()
 
    return {"success": True, "message": "Password changed successfully"}
 
 
# ── GET ALL USERS WITH ROLES (for role management) ───────────────
@app.get("/all-users")
def get_all_users():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, full_name, email, role
                FROM users
                ORDER BY role, full_name
            """)
        )
        users = [dict(row._mapping) for row in result]
    return users
 
 
# ── UPDATE USER ROLE ─────────────────────────────────────────────
@app.post("/update-role")
def update_role(user_id: int, new_role: str):
    valid_roles = ["employee", "manager", "admin"]
    if new_role not in valid_roles:
        return {"success": False, "message": "Invalid role"}
 
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE users SET role=:role WHERE id=:user_id"),
            {"role": new_role, "user_id": user_id}
        )
        conn.commit()
 
    return {"success": True}



# ==========================================================
# SALES DASHBOARD ROUTES
# ==========================================================

from typing import Optional


# ----------------------------------------------------------
# TEAM MEMBER IDS
# ----------------------------------------------------------

def _team_member_ids(manager_id: int, conn):

    rows = conn.execute(
        text("""
            SELECT employee_id
            FROM team_members
            WHERE manager_id=:manager_id
        """),
        {"manager_id": manager_id}
    ).fetchall()

    return [row.employee_id for row in rows]


# ----------------------------------------------------------
# CURRENT WEEK
# ----------------------------------------------------------

@app.get("/sales/current-week")
def sales_current_week():

    return {

        "week": current_week()

    }


# ----------------------------------------------------------
# ADD PROJECTION
# ----------------------------------------------------------

from typing import Optional

@app.post("/sales/projection")
def post_projection(
    user_id: int,
    week: int,
    customer: Optional[str] = "",
    product: Optional[str] = "",
    projected: Optional[int] = 0,
    price: Optional[float] = 0
):

    if week < current_week():

        return {

            "success": False,
            "message": "Projections can only be added for current week."

        }

    try:

        return add_projection(

            user_id=user_id,
            week=week,
            customer=customer,
            product=product,
            projected=projected,
            price=price

        )

    except Exception as e:

        return {

            "success": False,
            "message": str(e)

        }


# ----------------------------------------------------------
# GET SALES ROWS
# ----------------------------------------------------------

@app.get("/sales/rows")
def sales_rows(
    user_id: int,
    week: int,
    viewer_id: int,
    viewer_role: str
):
    if viewer_role == "admin":
        pass  # admin can view anyone
    elif viewer_role == "manager":
        # manager can view their own rows OR their team members'
        if viewer_id != user_id:
            with engine.connect() as conn:
                team = _team_member_ids(viewer_id, conn)
            if user_id not in team:
                return {"success": False, "message": "Not your team member"}
    else:
        # employee can only view their own rows
        if viewer_id != user_id:
            return {"success": False, "message": "Access denied"}

    return {"rows": get_sales(user_id, week)}


# ----------------------------------------------------------
# GET WEEKS
# ----------------------------------------------------------

@app.get("/sales/weeks")
def sales_weeks(
    user_id: int,
    viewer_id: int,
    viewer_role: str
):
    if viewer_role == "admin":
        pass  # admin can view anyone
    elif viewer_role == "manager":
        # manager can view own weeks OR team members'
        if viewer_id != user_id:
            with engine.connect() as conn:
                team = _team_member_ids(viewer_id, conn)
            if user_id not in team:
                return {"success": False}
    else:
        if viewer_id != user_id:
            return {"success": False}

    return {"weeks": get_all_weeks(user_id)}


# ----------------------------------------------------------
# UPDATE ACHIEVED
# ----------------------------------------------------------

@app.put("/sales/achieved")
def sales_achieved(
    user_id: int,
    week: int,
    customer: str,
    product: str,
    achieved: int
):

    if week < current_week():
        return {
            "success": False,
            "message": "Only current or future weeks are editable."
        }

    try:

        return update_achieved(

            user_id,
            week,
            customer,
            product,
            achieved

        )

    except Exception as e:

        return {

            "success": False,
            "message": str(e)

        }


# ----------------------------------------------------------
# TEAM SALES
# ----------------------------------------------------------

@app.get("/sales/team")
def sales_team(
    manager_id: int,
    week: int,
    viewer_role: str
):

    with engine.connect() as conn:

        if viewer_role == "admin":

            rows = conn.execute(
                text("""
                    SELECT id
                    FROM users
                    WHERE role='employee'
                """)
            ).fetchall()

            employee_ids = [row.id for row in rows]

        else:

            employee_ids = _team_member_ids(
                manager_id,
                conn
            )

    data = get_sales_for_employees(
        employee_ids,
        week
    )

    names = {}

    if employee_ids:

        placeholders = ",".join(
            str(i)
            for i in employee_ids
        )

        with engine.connect() as conn:

            rows = conn.execute(
                text(f"""
                    SELECT
                    id,
                    full_name

                    FROM users

                    WHERE id IN ({placeholders})
                """)
            ).fetchall()

        names = {

            row.id: row.full_name

            for row in rows

        }

    result = []

    for emp_id in employee_ids:

        result.append({

            "id": emp_id,
            "name": names.get(
                emp_id,
                f"Employee {emp_id}"
            ),
            "rows": data.get(
                emp_id,
                []
            )

        })

    return {

        "week": week,
        "employees": result

    }


# ----------------------------------------------------------
# ADMIN / MANAGER EDIT PROJECTION
# ----------------------------------------------------------

@app.put("/sales/projection/admin-edit")
def admin_edit_projection_route(
    viewer_role: str,
    user_id: int,
    week: int,
    customer: str,
    product: str,
    new_qty: int
):

    if viewer_role not in [

        "admin",
        "manager"

    ]:

        return {

            "success": False

        }

    try:

        return admin_update_projection(

            user_id,
            week,
            customer,
            product,
            new_qty

        )

    except Exception as e:

        return {

            "success": False,
            "message": str(e)

        }


# ----------------------------------------------------------
# CHANGE REQUEST
# ----------------------------------------------------------

@app.post("/sales/change-request")
def sales_change_request(
    employee_id: int,
    week: int,
    customer: str,
    product: str,
    old_qty: int,
    new_qty: int,
    reason: str
):

    return raise_change_request(

        employee_id,
        week,
        customer,
        product,
        old_qty,
        new_qty,
        reason

    )


# ----------------------------------------------------------
# LIST CHANGE REQUESTS
# ----------------------------------------------------------

@app.get("/sales/change-requests")
def list_change_requests(
    viewer_id: int,
    viewer_role: str,
    status: Optional[str] = None
):

    if viewer_role == "employee":

        requests = get_change_requests(

            employee_ids=[viewer_id],
            status=status

        )

    elif viewer_role == "manager":

        with engine.connect() as conn:

            team = _team_member_ids(
                viewer_id,
                conn
            )

        requests = get_change_requests(

            employee_ids=team,
            status=status

        )

    elif viewer_role == "admin":

        requests = get_change_requests(

            employee_ids=None,
            status=status

        )

    else:

        requests = []

    return {

        "requests": requests

    }


# ----------------------------------------------------------
# RESOLVE CHANGE REQUEST
# ----------------------------------------------------------

@app.post("/sales/change-request/resolve")
def resolve_request(
    request_id: str,
    action: str,
    manager_note: str = "",
    viewer_role: str = ""
):

    if viewer_role not in [

        "admin",
        "manager"

    ]:

        return {

            "success": False

        }

    try:

        return resolve_change_request(

            request_id,
            action,
            manager_note

        )

    except Exception as e:

        return {

            "success": False,
            "message": str(e)

        }

from fastapi.responses import FileResponse

from fastapi.responses import FileResponse

@app.get("/sales/download")
def download_sales():

    return FileResponse(
        FILE_NAME,
        filename="sales_tracker.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

from openpyxl import load_workbook

@app.get("/sales/debug")
def sales_debug():

    wb = load_workbook(FILE_NAME)
    output = {}

    for sheet in wb.sheetnames:
        ws = wb[sheet]
        rows = [row for row in ws.iter_rows(values_only=True)]
        output[sheet] = rows

    return output
@app.get("/sales/debug-path")
def debug_path():

    import os

    return {

        "cwd": os.getcwd(),

        "files": os.listdir()

    }
@app.get("/test123")
def test123():
    return {
        "ok": True
    }
import os

@app.get("/testfiles")
def testfiles():

    try:

        return {
            "cwd": os.getcwd(),
            "files": os.listdir(".")
        }

    except Exception as e:

        return {
            "error": str(e)
        }
@app.get("/sales/test-add")
def sales_test_add():

    try:

        return add_projection(
            user_id=11,
            week=current_week(),
            customer="XYZ Company",
            product="Switch",
            projected=25,
            price=800
        )

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ═══════════════════════════════════════════════════════
# TASK FILE ATTACHMENT
# ═══════════════════════════════════════════════════════
# Run once to add the column (idempotent):
#   ALTER TABLE tasks ADD COLUMN IF NOT EXISTS file_url TEXT;
#   ALTER TABLE tasks ADD COLUMN IF NOT EXISTS file_name TEXT;

import shutil, os as _os

UPLOAD_DIR = _os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", ".") + "/task_files"
_os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/submit-task-with-file")
async def submit_task_with_file(
    task_id: int,
    file: UploadFile = FastAPIFile(None)
):
    """
    Employee calls this instead of /update-task-status when submitting
    for review with an optional file attachment.
    Saves the file to the persistent volume and stores the path in tasks.
    """
    file_url  = None
    file_name = None

    if file and file.filename:
        safe_name = f"{task_id}_{file.filename.replace(' ', '_')}"
        dest      = f"{UPLOAD_DIR}/{safe_name}"
        with open(dest, "wb") as buf:
            shutil.copyfileobj(file.file, buf)
        file_url  = f"/task-file/{safe_name}"
        file_name = file.filename

    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE tasks
                SET status    = 'Pending Review',
                    file_url  = :file_url,
                    file_name = :file_name
                WHERE id = :task_id
            """),
            {"task_id": task_id, "file_url": file_url, "file_name": file_name}
        )
        conn.commit()

    return {"success": True, "file_url": file_url, "file_name": file_name}


from fastapi.responses import FileResponse as _FileResp

@app.get("/task-file/{filename}")
def serve_task_file(filename: str):
    path = f"{UPLOAD_DIR}/{filename}"
    if not _os.path.exists(path):
        return {"error": "File not found"}
    return _FileResp(path, filename=filename)


# ═══════════════════════════════════════════════════════
# TASK REMARKS (manager → employee corrections)
# ═══════════════════════════════════════════════════════
# Run once:
#   CREATE TABLE IF NOT EXISTS task_remarks (
#       id          SERIAL PRIMARY KEY,
#       task_id     INT NOT NULL,
#       manager_id  INT NOT NULL,
#       employee_id INT NOT NULL,
#       remark      TEXT NOT NULL,
#       status      TEXT DEFAULT 'pending',   -- pending | resolved
#       created_at  TIMESTAMP DEFAULT NOW()
#   );

@app.post("/send-remark")
def send_remark(
    task_id:     int,
    manager_id:  int,
    employee_id: int,
    remark:      str
):
    """
    Manager sends a correction remark on a task.
    Also resets the task status back to 'In Progress' so employee
    can fix and re-submit.
    """
    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO task_remarks
                (task_id, manager_id, employee_id, remark, status)
                VALUES
                (:task_id, :manager_id, :employee_id, :remark, 'pending')
            """),
            {
                "task_id":     task_id,
                "manager_id":  manager_id,
                "employee_id": employee_id,
                "remark":      remark
            }
        )

        # Push task back to In Progress so employee can re-submit
        conn.execute(
            text("""
                UPDATE tasks
                SET status = 'In Progress'
                WHERE id = :task_id
            """),
            {"task_id": task_id}
        )

        conn.commit()

    return {"success": True}


@app.get("/task-remarks")
def get_task_remarks(employee_id: int):
    """
    Returns all pending remarks for an employee across all tasks.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT
                    tr.id,
                    tr.task_id,
                    tr.remark,
                    tr.status,
                    tr.created_at,
                    t.title  AS task_title,
                    u.full_name AS manager_name
                FROM task_remarks tr
                JOIN tasks t  ON tr.task_id    = t.id
                JOIN users u  ON tr.manager_id = u.id
                WHERE tr.employee_id = :employee_id
                ORDER BY tr.created_at DESC
            """),
            {"employee_id": employee_id}
        ).fetchall()

    return [dict(r._mapping) for r in rows]


@app.put("/resolve-remark")
def resolve_remark(remark_id: int):
    """Employee marks a remark as resolved after fixing."""
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE task_remarks SET status='resolved' WHERE id=:id"),
            {"id": remark_id}
        )
        conn.commit()
    return {"success": True}


@app.get("/manager-remarks")
def get_manager_remarks(manager_id: int):
    """Returns all remarks sent by this manager, with current task status."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT
                    tr.id,
                    tr.task_id,
                    tr.remark,
                    tr.status      AS remark_status,
                    tr.created_at,
                    t.title        AS task_title,
                    t.status       AS task_status,
                    u.full_name    AS employee_name
                FROM task_remarks tr
                JOIN tasks t  ON tr.task_id     = t.id
                JOIN users u  ON tr.employee_id = u.id
                WHERE tr.manager_id = :manager_id
                ORDER BY tr.created_at DESC
            """),
            {"manager_id": manager_id}
        ).fetchall()

    return [dict(r._mapping) for r in rows]

@app.post("/meetings/create")
def create_meeting(req: MeetingRequest):

    with engine.begin() as conn:

        conflict = conn.execute(
            text("""
            SELECT id
            FROM meetings
            WHERE meeting_date=:meeting_date
            AND organizer_id=:organizer_id
            AND (
                start_slot < :new_end
                AND end_slot > :new_start
            )
            """),
            {
                "meeting_date": req.meeting_date,
                "organizer_id": req.organizer_id,
                "new_start": req.start_slot,
                "new_end": req.end_slot
            }
        ).fetchone()

        if conflict:
            return {
                "success": False,
                "message": "Organizer already has a meeting"
            }

        meeting_id = conn.execute(
            text("""
            INSERT INTO meetings(
                title,
                description,
                organizer_id,
                meeting_date,
                start_slot,
                end_slot,
                location
            )
            VALUES(
                :title,
                :description,
                :organizer_id,
                :meeting_date,
                :start_slot,
                :end_slot,
                :location
            )
            RETURNING id
            """),
            req.model_dump()
        ).scalar()

        for user_id in req.attendees:

            conn.execute(
                text("""
                INSERT INTO meeting_attendees(
                    meeting_id,
                    user_id
                )
                VALUES(
                    :meeting_id,
                    :user_id
                )
                """),
                {
                    "meeting_id": meeting_id,
                    "user_id": user_id
                }
            )

    return {
        "success": True,
        "meeting_id": meeting_id
    }
