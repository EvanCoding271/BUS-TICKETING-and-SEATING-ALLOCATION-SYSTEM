<<<<<<< HEAD
# CityBus Transport - Ticket Booking and Seat Allocation

## Overview
Centralized web app for online ticket booking, real-time seat allocation, QR ticketing, and role-based employee portals.

## Tech stack
- Frontend: HTML, CSS, JS (static)
- Backend: Python, FastAPI
- Database: Supabase (Postgres)
- Auth: JWT, bcrypt
- Deployment: Vercel (frontend), Render/Railway recommended for backend

## Quickstart (local)
1. Clone repo
2. Create virtualenv: python -m venv venv && source venv/bin/activate
3. Install: pip install -r backend/requirements.txt
4. Create `.env` from `.env.example` and set DATABASE_URL and JWT_SECRET
5. Run DB migrations: psql $DATABASE_URL -f database/supabase_schema.sql
6. Start backend: uvicorn backend.main:app --reload --port 8000
7. Serve frontend: open `frontend/index.html` in browser or use simple HTTP server

## API endpoints
- POST /auth/user/register
- POST /auth/user/login
- POST /auth/employee/login
- POST /bookings/reserve
- POST /qr/generate/{booking_id}
- POST /qr/validate

(See `backend/routers` for full list)

## Deployment
Follow the detailed deployment tutorial in `DEPLOYMENT.md`.
=======
# CityBus Transport - Ticket Booking and Seat Allocation

## Overview
Centralized web app for online ticket booking, real-time seat allocation, QR ticketing, and role-based employee portals.

## Tech stack
- Frontend: HTML, CSS, JS (static)
- Backend: Python, FastAPI
- Database: Supabase (Postgres)
- Auth: JWT, bcrypt
- Deployment: Vercel (frontend), Render/Railway recommended for backend

## Quickstart (local)
1. Clone repo
2. Create virtualenv: python -m venv venv && source venv/bin/activate
3. Install: pip install -r backend/requirements.txt
4. Create `.env` from `.env.example` and set DATABASE_URL and JWT_SECRET
5. Run DB migrations: psql $DATABASE_URL -f database/supabase_schema.sql
6. Start backend: uvicorn backend.main:app --reload --port 8000
7. Serve frontend: open `frontend/index.html` in browser or use simple HTTP server

## API endpoints
- POST /auth/user/register
- POST /auth/user/login
- POST /auth/employee/login
- POST /bookings/reserve
- POST /qr/generate/{booking_id}
- POST /qr/validate

(See `backend/routers` for full list)

## Deployment
Follow the detailed deployment tutorial in `DEPLOYMENT.md`.
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0
