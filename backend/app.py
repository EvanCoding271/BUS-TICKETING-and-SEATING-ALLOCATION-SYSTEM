import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.database.connection import database
from backend.routers import auth_user, auth_employee, bookings, qr, routes, schedules, payments, finance


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database.is_connected:
        await database.connect()
    try:
        yield
    finally:
        if database.is_connected:
            await database.disconnect()


app = FastAPI(
    title="CityBus Transport API",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/api"  # FIX: tells FastAPI it is mounted under /api on Vercel
)

origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_user.router)
app.include_router(auth_employee.router)
app.include_router(bookings.router)
app.include_router(qr.router)
app.include_router(routes.router)
app.include_router(schedules.router)
app.include_router(payments.router)
app.include_router(finance.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "CITYBUS API"}
