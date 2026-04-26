# Task Manager API

A simple REST API built with FastAPI and SQLite to manage daily tasks. Developed to demonstrate backend skills including CRUD operations, data validation, and database integration.

## Features
- Full CRUD (Create, Read, Update, Delete) for tasks
- Automatic interactive documentation (Swagger UI)
- Lightweight SQLite database (no external server setup)
- Clean architecture with separate modules for models, schemas, and database

## Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pydantic

## How to Run Locally
1. Clone the repository:  `git clone ...`
2. Install dependencies:  `pip install -r requirements.txt`
3. Start the server:      `uvicorn main:app --reload`
4. Open http://127.0.0.1:8000/docs to explore the API

## API Endpoints

| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| POST   | /tasks/        | Create a new task    |
| GET    | /tasks/        | List all tasks       |
| GET    | /tasks/{id}    | Get a single task    |
| PUT    | /tasks/{id}    | Update a task        |
| DELETE | /tasks/{id}    | Delete a task        |

## Author
Matheus Valério Souto Monteiro – [LinkedIn](https://www.linkedin.com/in/matheus-souto-monteiro/)
