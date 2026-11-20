
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


# =========================
# DATABASE CONNECTION
# =========================

connectionn = sqlite3.connect(
    "myTestDB",
    check_same_thread=False
)

cursorr = connectionn.cursor()


# =========================
# CREATE TABLE
# =========================

cursorr.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

connectionn.commit()


# =========================
# PYDANTIC MODEL
# =========================

class Todo(BaseModel):
    title: str
    status: str


# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():
    return {
        "message": "SQLite connection established"
    }


# =========================
# CREATE TODO
# =========================

@app.post("/todos", status_code=201)
def create_todo(todo: Todo):

    cursorr.execute(
        "INSERT INTO todos (title, status) VALUES (?, ?)",
        (todo.title, todo.status)
    )

    connectionn.commit()

    todo_id = cursorr.lastrowid

    return {
        "message": "Todo created successfully",
        "id": todo_id,
        "title": todo.title,
        "status": todo.status
    }


# =========================
# GET ALL TODOS
# =========================

@app.get("/todos")
def get_all_todos():

    cursorr.execute("SELECT * FROM todos")

    todos = cursorr.fetchall()

    return [
        {
            "id": todo[0],
            "title": todo[1],
            "status": todo[2]
        }
        for todo in todos
    ]


# =========================
# GET TODO BY ID
# =========================

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):

    cursorr.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    )

    todo = cursorr.fetchone()

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return {
        "id": todo[0],
        "title": todo[1],
        "status": todo[2]
    }


# =========================
# UPDATE TODO
# =========================

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):

    cursorr.execute(
        """
        UPDATE todos
        SET title = ?, status = ?
        WHERE id = ?
        """,
        (todo.title, todo.status, todo_id)
    )

    connectionn.commit()

    if cursorr.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return {
        "message": "Todo updated successfully",
        "id": todo_id,
        "title": todo.title,
        "status": todo.status
    }


# =========================
# DELETE TODO
# =========================

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    cursorr.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )

    connectionn.commit()

    if cursorr.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return {
        "message": "Todo deleted successfully",
        "id": todo_id
    }
