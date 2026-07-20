from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task API",
    description="A simple CRUD API built using FastAPI",
    version="1.0.0"
)
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Push Project to GitHub",
        "done": True
    }
]

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    title = task.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    next_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):

    # Find task
    for task in tasks:
        if task["id"] == task_id:

            # Update title if provided
            if task_update.title is not None:
                title = task_update.title.strip()

                if not title:
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )

                task["title"] = title

            # Update done if provided
            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    # Task not found
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )