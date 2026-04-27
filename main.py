from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Task Manager API",
    description="Simple CRUD API for managing tasks — built with FastAPI & SQLite",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "defaultModelsExpandDepth": -1,
    },
)

# ---------- PÁGINA INICIAL (HOME) ----------
@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Manager API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                text-align: center;
                padding: 20px;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                letter-spacing: 1px;
            }
            .emoji {
                font-size: 3rem;
                margin-bottom: 15px;
            }
            p {
                font-size: 1.2rem;
                margin-bottom: 15px;
                line-height: 1.6;
            }
            .features {
                text-align: left;
                margin: 20px 0;
                background: rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 20px;
                list-style-type: none;
            }
            .features li {
                margin: 8px 0;
                font-size: 1rem;
                display: flex;
                align-items: center;
            }
            .features li::before {
                content: "✅";
                margin-right: 10px;
            }
            .buttons {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                justify-content: center;
                margin-top: 25px;
            }
            .btn {
                background-color: white;
                color: #1e3c72;
                padding: 12px 24px;
                border-radius: 30px;
                text-decoration: none;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                display: inline-block;
            }
            .btn:hover {
                background-color: #f0f0f0;
                transform: translateY(-2px);
                box-shadow: 0 6px 14px rgba(0,0,0,0.3);
            }
            .footer {
                margin-top: 30px;
                font-size: 0.9rem;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🚀</div>
            <h1>Task Manager API</h1>
            <p>A simple and modern REST API to manage your daily tasks, built with <strong>FastAPI</strong> and <strong>SQLite</strong>.</p>
            <ul class="features">
                <li>Full CRUD operations (Create, Read, Update, Delete)</li>
                <li>Interactive API documentation (Swagger UI)</li>
                <li>Clean architecture and easy to test endpoints</li>
            </ul>
            <div class="buttons">
                <a href="/docs" class="btn">📖 Swagger Docs</a>
                <a href="/redoc" class="btn">📘 ReDoc</a>
                <a href="https://github.com/09116751-bit/API" target="_blank" class="btn">💻 GitHub Repo</a>
            </div>
            <div class="footer">
                Made by Matheus Valério Souto Monteiro
            </div>
        </div>
    </html>
    """
    return HTMLResponse(content=html_content)

# ---------- DEPENDÊNCIA DO BANCO ----------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- ROTAS DA API (CRUD COMPLETO) ----------

@app.post("/tasks/", response_model=schemas.TaskResponse, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=list[schemas.TaskResponse], tags=["Tasks"])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}