<<<<<<< HEAD
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..auth.password import hash_password, verify_password
from ..auth.jwt_handler import create_access_token
from ..database.connection import database

router = APIRouter(prefix="/auth/user", tags=["auth_user"])

class RegisterSchema(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str

@router.post("/register")
async def register(payload: RegisterSchema):
    # check unique email
    query = "SELECT id FROM users WHERE email = :email"
    row = await database.fetch_one(query, values={"email": payload.email})
    if row:
        raise HTTPException(400, "Email already registered")
    hashed = hash_password(payload.password)
    insert = """INSERT INTO users (full_name,email,phone,password_hash,created_at)
                VALUES (:full_name,:email,:phone,:password_hash,now()) RETURNING id"""
    user_id = await database.execute(insert, values={
        "full_name": payload.full_name,
        "email": payload.email,
        "phone": payload.phone,
        "password_hash": hashed
    })
    return {"id": user_id}

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(payload: LoginSchema):
    q = "SELECT id, password_hash, role FROM users WHERE email = :email"
    user = await database.fetch_one(q, values={"email": payload.email})
    if not user or not verify_password(payload.password, user['password_hash']):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user['id'], "role": user.get('role','passenger')})
    return {"access_token": token}
=======
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..auth.password import hash_password, verify_password
from ..auth.jwt_handler import create_access_token
from ..database.connection import database

router = APIRouter(prefix="/auth/user", tags=["auth_user"])

class RegisterSchema(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str

@router.post("/register")
async def register(payload: RegisterSchema):
    # check unique email
    query = "SELECT id FROM users WHERE email = :email"
    row = await database.fetch_one(query, values={"email": payload.email})
    if row:
        raise HTTPException(400, "Email already registered")
    hashed = hash_password(payload.password)
    insert = """INSERT INTO users (full_name,email,phone,password_hash,created_at)
                VALUES (:full_name,:email,:phone,:password_hash,now()) RETURNING id"""
    user_id = await database.execute(insert, values={
        "full_name": payload.full_name,
        "email": payload.email,
        "phone": payload.phone,
        "password_hash": hashed
    })
    return {"id": user_id}

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(payload: LoginSchema):
    q = "SELECT id, password_hash, role FROM users WHERE email = :email"
    user = await database.fetch_one(q, values={"email": payload.email})
    if not user or not verify_password(payload.password, user['password_hash']):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user['id'], "role": user.get('role','passenger')})
    return {"access_token": token}
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0
