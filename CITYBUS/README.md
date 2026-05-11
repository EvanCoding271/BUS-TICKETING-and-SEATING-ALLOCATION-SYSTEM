# CityBus Transport

CityBus Transport is a complete web-based ticket booking and seat allocation system for passenger users and employee portals. The application uses a static HTML/CSS/JavaScript frontend and a Python FastAPI backend with Supabase/PostgreSQL as the data layer.

## Project structure

- `frontend/` - full static frontend with passenger and employee portals
- `backend/` - FastAPI backend services, JWT auth, role-based access, business routing
- `database/` - Supabase SQL schema for production-ready PostgreSQL
- `vercel.json` - deployment metadata for Vercel static frontend and backend

## Quick start

1. Create a Python virtual environment:
   ```powershell
   cd c:\CITYBUS\backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and provide your Supabase/PostgreSQL connection details.
4. Run database migration:
   ```powershell
   psql "%DATABASE_URL%" -f ..\database\supabase_schema.sql
   ```
5. Start the FastAPI backend:
   ```powershell
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
6. Open the frontend by serving `frontend/` through a local static server or opening `frontend/index.html` in your browser.

## Backend endpoints

- `POST /auth/user/register`
- `POST /auth/user/login`
- `POST /auth/employee/login`
- `POST /bookings/reserve`
- `POST /bookings/confirm`
- `GET /bookings/history`
- `POST /qr/generate/{booking_id}`
- `POST /qr/validate`
- `GET /routes/list`
- `POST /routes/create`
- `POST /schedules/create`
- `POST /payments/process`
- `POST /payments/refund`
- `GET /finance/summary`

## Deployment notes

- Frontend is static and works well on Vercel.
- Backend can be deployed on Vercel Python support, but Render or Railway is recommended for a stateful PostgreSQL-backed FastAPI API.
- See `DEPLOYMENT.md` for the full detailed deployment tutorial.
