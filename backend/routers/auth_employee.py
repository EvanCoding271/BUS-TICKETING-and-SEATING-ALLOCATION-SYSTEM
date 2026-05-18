from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# 🛠️ FIXED: Removed '..'
from auth.password import hash_password, verify_password
from auth.jwt_handler import create_access_token
from database.connection import database

router = APIRouter(prefix="/auth/employee", tags=["auth_employee"])

@router.post("/login")
async def login(payload: EmployeeLoginSchema):
    query = """
      SELECT e.id, e.password_hash, r.name AS role
      FROM employees e
      JOIN roles r ON e.role_id = r.id
      WHERE e.email = :email AND e.is_active = true
    """
    row = await database.fetch_one(query, values={"email": payload.email})
    if not row or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": row["id"], "role": row["role"]})
    return {"access_token": token, "role": row["role"]}
