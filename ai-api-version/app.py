from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Task API",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        e = {"loc": err["loc"], "msg": err["msg"], "type": err["type"]}
        if "ctx" in err and "error" in err["ctx"]:
            e["msg"] = str(err["ctx"]["error"])
        errors.append(e)
    return JSONResponse(status_code=400, content={"detail": errors})


tasks = []
next_id = 1


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("title must not be empty or whitespace only")
        return stripped


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str | None) -> str | None:
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("title must not be empty or whitespace only")
            return stripped
        return v


class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(body: TaskCreate):
    global next_id
    task = {"id": next_id, "title": body.title, "done": False}
    tasks.append(task)
    next_id += 1
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, body: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if body.title is not None:
                task["title"] = body.title
            if body.done is not None:
                task["done"] = body.done
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")
