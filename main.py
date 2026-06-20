from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware



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
                (task_id,employee_id,task_title)
                VALUES
                (:task_id,:employee_id,:task_title)
            """),
            {
                "task_id":task.id,
                "employee_id":task.assigned_to,
                "task_title":task.title
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

@app.get("/manager-stats")
def manager_stats():

    with engine.connect() as conn:

        employees = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM users
                WHERE role='employee'
            """)
        ).scalar()

        total_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
            """)
        ).scalar()

        completed_tasks = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE status='Completed'
            """)
        ).scalar()

    productivity = 0

    if total_tasks > 0:
        productivity = round(
            (completed_tasks/total_tasks)*100
        )

    return {
        "employees": employees,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "productivity": productivity
    }


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

        conn.execute(
            text("""
                UPDATE tasks
                SET status='Completed'
                WHERE id=:id
            """),
            {"id":task_id}
        )

        conn.commit()

    return {"success":True}


@app.get("/review-tasks")
def review_tasks():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM tasks WHERE status='Pending Review' ORDER BY id DESC")
        )
        tasks = [dict(row._mapping) for row in result]
    return tasks
@app.get("/team")
def get_team(manager_id:int):

    with engine.connect() as conn:

        data = conn.execute(
            text("""
                SELECT users.id,
                       users.full_name,
                       users.email
                FROM team_members
                JOIN users
                ON team_members.employee_id = users.id
                WHERE manager_id=:manager_id
            """),
            {"manager_id":manager_id}
        ).fetchall()

    result=[]

    for row in data:

        result.append({
            "id":row.id,
            "full_name":row.full_name,
            "email":row.email
        })

    return result


@app.get("/employees")
def employees():

    with engine.connect() as conn:

        data = conn.execute(
            text("""
                SELECT id,
                       full_name,
                       email
                FROM users
                WHERE role='employee'
            """)
        ).fetchall()

    result=[]

    for row in data:

        result.append({
            "id":row.id,
            "full_name":row.full_name,
            "email":row.email
        })

    return result


@app.post("/team/add")
def add_team_member(manager_id:int,
                    employee_id:int):

    with engine.connect() as conn:

        exists = conn.execute(
            text("""
                SELECT *
                FROM team_members
                WHERE manager_id=:manager_id
                AND employee_id=:employee_id
            """),
            {
                "manager_id":manager_id,
                "employee_id":employee_id
            }
        ).fetchone()

        if exists:

            return {
                "success":False,
                "message":"Already in team"
            }

        conn.execute(
            text("""
                INSERT INTO team_members
                (manager_id,employee_id)
                VALUES
                (:manager_id,:employee_id)
            """),
            {
                "manager_id":manager_id,
                "employee_id":employee_id
            }
        )

        conn.commit()

    return {"success":True}



@app.post("/team/remove")
def remove_team_member(manager_id:int,
                       employee_id:int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM team_members
                WHERE manager_id=:manager_id
                AND employee_id=:employee_id
            """),
            {
                "manager_id":manager_id,
                "employee_id":employee_id
            }
        )

        conn.commit()

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
                    COUNT(tasks.id) AS task_count
                FROM team_members

                JOIN users
                ON team_members.employee_id = users.id

                LEFT JOIN tasks
                ON tasks.assigned_to = users.id
                AND LOWER(tasks.status)!='completed'

                WHERE team_members.manager_id=:manager_id

                GROUP BY
                users.id,
                users.full_name,
                users.email
            """),
            {"manager_id":manager_id}
        ).fetchall()

    result=[]

    for row in data:

        result.append({
            "id":row.id,
            "full_name":row.full_name,
            "email":row.email,
            "task_count":row.task_count
        })

    return result
