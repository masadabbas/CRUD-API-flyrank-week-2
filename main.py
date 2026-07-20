from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task Management API",
    description="""
A beginner-friendly CRUD API built using FastAPI.

Features:
- Create Tasks
- Read Tasks
- Update Tasks
- Delete Tasks

Data is stored in memory.
Restarting the server resets all tasks.
""",
    version="1.0.0",
    contact={
        "name": "Muhammad Asad Abbas",
        "email": "m.asadabbas2973@gmail.com"
    }
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

TASK_TAG = "Tasks"

@app.get(
    "/",
    summary="API Information",
    description="Returns basic information about the Task Management API."
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Checks whether the server is running."
)
def health():
    return {
        "status": "ok"
    }

@app.get(
    "/tasks",
    summary="Get All Tasks",
    description="Returns a list of all available tasks."
)
def get_tasks():
    return tasks

@app.get(
    "/tasks/{task_id}",
    tags=[TASK_TAG],
    summary="Get Task",
    responses={
        200: {"description": "Task found successfully"},
        404: {"description": "Task not found"}
    }
)
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )

@app.post(
    "/tasks",
    tags=[TASK_TAG],
    status_code=201,
    summary="Create Task",
    responses={
    201: {"description":"Task Created"},
    400: {"description":"Invalid Request"}
}
)
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

@app.put(
    "/tasks/{task_id}",
    tags=[TASK_TAG],
    summary="Update Task",
    responses={
    200: {"description":"Task Updated"},
    400: {"description":"Invalid Data"},
    404: {"description":"Task Not Found"}
}
)
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

@app.delete(
    "/tasks/{task_id}",
    tags=[TASK_TAG],
    status_code=204,
    summary="Delete Task",
    responses={
    204: {"description":"Task Deleted"},
    404: {"description":"Task Not Found"}
}
)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )