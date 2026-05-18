import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the repository root is on sys.path so backend imports work in Vercel's serverless execution.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.database.connection import database
from backend.routers import auth_user, auth_employee, bookings, qr, routes, schedules, payments, finance

app = FastAPI(title="CityBus Transport API", version="1.0.0")

origins = [origin.strip() for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000').split(',') if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Change ONLY these two lines in your backend/app.py:
app.include_router(auth_user.router, prefix="/api", tags=["User Auth"])
app.include_router(auth_employee.router, prefix="/api", tags=["Employee Auth"])

# Keep the rest exactly the same:
app.include_router(bookings.router, prefix="/api", tags=["Bookings"])
app.include_router(qr.router, prefix="/api", tags=["QR"])
app.include_router(routes.router, prefix="/api", tags=["Routes"])
app.include_router(schedules.router, prefix="/api", tags=["Schedules"])
app.include_router(payments.router, prefix="/api", tags=["Payments"])
app.include_router(finance.router, prefix="/api", tags=["Finance"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
