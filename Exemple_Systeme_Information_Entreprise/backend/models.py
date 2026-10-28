"""Accès aux données : fonctions SQL simples pour l'exemple."""
from .database import get_connection

def list_employees():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, full_name, email, department, job_title FROM employees ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]

def get_employee(employee_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, full_name, email, department, job_title FROM employees WHERE id = ?",
            (employee_id,)
        ).fetchone()
        return dict(row) if row else None

def create_employee(data: dict):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO employees (full_name, email, department, job_title) VALUES (?, ?, ?, ?)",
            (data["full_name"], data["email"], data["department"], data["job_title"])
        )
        conn.commit()
        return get_employee(cursor.lastrowid)

def update_employee(employee_id: int, data: dict):
    with get_connection() as conn:
        cursor = conn.execute(
            """UPDATE employees
               SET full_name = ?, email = ?, department = ?, job_title = ?
               WHERE id = ?""",
            (data["full_name"], data["email"], data["department"], data["job_title"], employee_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None
    return get_employee(employee_id)

def delete_employee(employee_id: int):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        conn.commit()
        return cursor.rowcount > 0
