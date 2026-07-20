# Task Management API

A beginner-friendly REST API built with **FastAPI**.

## Features

- Create Tasks
- Read Tasks
- Update Tasks
- Delete Tasks
- Automatic Swagger Documentation
- In-Memory Data Storage

---

## Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Pydantic
- Git
- GitHub

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/fastapi-task-api.git
```

Go inside the project

```bash
cd fastapi-task-api
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn app:app --reload
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```
## Swagger Preview

![Swagger UI](swagger.png)
---

## Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API Information |
| GET | /health | Health Check |
| GET | /tasks | Get All Tasks |
| GET | /tasks/{id} | Get Single Task |
| POST | /tasks | Create Task |
| PUT | /tasks/{id} | Update Task |
| DELETE | /tasks/{id} | Delete Task |

---

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Learn FastAPI\"}"
```

---

## Example Response

```json
{
  "id": 4,
  "title": "Learn FastAPI",
  "done": false
}
```

---

## Project Structure

```
task-api/
│
├── app.py
├── requirements.txt
├── README.md
├── swagger-ui.png
├── .gitignore
└── venv/
```

# AI vs Me (Stage 7 – AI Rematch)

## AI Prompt

I asked an AI assistant to build the same REST API that I had already implemented manually.

**Prompt:**

> Build a REST API using Python and FastAPI.
>
> Requirements:
>
> * Use only in-memory storage (Python list). Do not use any database.
> * Implement the following endpoints:
>
>   * `GET /` – Return API name and version.
>   * `GET /health` – Return `{"status":"ok"}`.
>   * `GET /tasks` – Return all tasks.
>   * `GET /tasks/{id}` – Return a single task by ID and return `404` if it does not exist.
>   * `POST /tasks` – Accept JSON containing a task title, automatically assign the next ID, set `done` to `false`, reject empty or whitespace-only titles with HTTP `400`, and return HTTP `201`.
>   * `PUT /tasks/{id}` – Update the title and/or done status, reject empty titles with HTTP `400`, and return `404` if the task does not exist.
>   * `DELETE /tasks/{id}` – Delete a task, return HTTP `204`, and return `404` if the task does not exist.
> * Use Pydantic models for request validation.
> * Enable FastAPI Swagger documentation.
> * Keep the implementation in a single `app.py` file.

---

## Running the AI Version

The AI-generated code was saved in a separate folder (`ai-version/`) so that my hand-written implementation remained unchanged.

The application started successfully using:

```bash
uvicorn app:app --reload
```

I tested the generated API using the same `curl` commands from my manual implementation.

### Test Results

| Test               | Expected       | Result   |
| ------------------ | -------------- | -------- |
| POST /tasks        | 201 Created    | ✅ Passed |
| GET /tasks         | 200 OK         | ✅ Passed |
| GET /tasks/{id}    | 200 / 404      | ✅ Passed |
| PUT /tasks/{id}    | 200 OK         | ✅ Passed |
| DELETE /tasks/{id} | 204 No Content | ✅ Passed |
| Swagger (/docs)    | Available      | ✅ Passed |

The generated API started successfully on the first attempt and all CRUD operations worked correctly.

---

## What the AI Did Better

After comparing the AI-generated code with my own implementation, I noticed several improvements:

* It used **response models** (`TaskResponse`) for cleaner API responses.
* It implemented **custom validation handling**, converting FastAPI's default validation errors into HTTP `400` responses.
* It used **Pydantic Field** and **field_validator**, making validation more structured and reusable.
* It separated request and response models more clearly than my original implementation.
* The code was concise while still remaining readable.

I reviewed each of these improvements and understand how they work.

---

## What the AI Got Wrong or Handled Differently

Although the generated code worked well, I noticed a few differences from my own implementation:

* It returned `"Task not found"` for every missing task instead of including the requested task ID in the error message (for example, `"Task 99 not found"`).
* It used a global `next_id` counter instead of calculating the next ID from the existing task list.
* The initial task list was empty, whereas my hand-built version started with sample tasks for easier testing.
* The validation error response format was different from my own implementation because it used a custom exception handler.

These differences are design choices rather than bugs, but they show that an AI may make reasonable assumptions when requirements are not fully specified.

---

## What My Prompt Forgot to Specify

While reviewing the generated code, I realized that my prompt did not explicitly define several implementation details:

* Whether the API should start with sample tasks or an empty list.
* The exact format of error messages.
* How IDs should be generated (incremental counter vs. calculating the maximum existing ID).
* Whether custom exception handlers should be used.
* Whether response models should be implemented.

Because these details were not specified, the AI made its own design decisions.

---

## Prompt Improvement (Second Attempt)

For the second attempt, I improved my prompt by specifying:

* Exact error message format.
* Initial sample task data.
* ID generation strategy.
* Response format requirements.
* Validation behaviour.

The regenerated version matched my original implementation much more closely.

---

## Reflection

This exercise showed me that writing a precise specification is just as important as writing code. The AI generated a working API very quickly, but it still made several design decisions where my prompt was ambiguous. Because I had already built the project manually, I was able to review the generated code confidently, understand its improvements, and identify differences. This reinforced the idea that AI is a powerful development assistant, but it still requires clear requirements and human review.


---


## Author

Muhammad Asad Abbas