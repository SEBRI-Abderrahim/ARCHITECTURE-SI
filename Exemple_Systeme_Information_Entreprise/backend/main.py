from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from . import models
from .schemas import Employee, EmployeeCreate, EmployeeUpdate

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"

app = FastAPI(
    title="Système d'information — Gestion des employés",
    version="1.0.0",
    description="API pédagogique CRUD pour gérer les employés."
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/employees", response_model=list[Employee])
def list_employees():
    return models.list_employees()

@app.get("/api/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    employee = models.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employé introuvable")
    return employee

@app.post("/api/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate):
    try:
        return models.create_employee(employee.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Cette adresse e-mail existe déjà")

@app.put("/api/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: EmployeeUpdate):
    try:
        updated = models.update_employee(employee_id, employee.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Cette adresse e-mail existe déjà")
    if not updated:
        raise HTTPException(status_code=404, detail="Employé introuvable")
    return updated

@app.delete("/api/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    if not models.delete_employee(employee_id):
        raise HTTPException(status_code=404, detail="Employé introuvable")
    return None
