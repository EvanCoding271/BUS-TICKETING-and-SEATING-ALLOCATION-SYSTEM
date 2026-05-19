# CityBus Transport Deployment Guide

This guide contains the full detailed deployment tutorial for the CityBus Transport application in a separate document from the main README.

## Part 1 — Local Development Setup

### 1. Install Python
- Download Python 3.11 or 3.12 from https://www.python.org/downloads/.
- Install with the `Add Python to PATH` option enabled.
- Verify in PowerShell:
  ```powershell
  python --version
  ```

### 2. Install VS Code
- Download and install Visual Studio Code from https://code.visualstudio.com/.
- Open the `c:\CITYBUS` folder in VS Code.

### 3. Install recommended extensions
- Python
- Pylance
- GitLens (optional)
- REST Client (optional)
- YAML (optional)

### 4. Create folders
The repository already contains the required structure. Confirm these top-level folders exist:
- `frontend/`
- `backend/`
- `database/`

### 5. Setup virtual environment
From `c:\CITYBUS` in PowerShell:
```powershell
cd c:\CITYBUS\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 6. Install requirements
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Run frontend
The frontend is static. Use one of these options:
- Open `c:\CITYBUS\frontend\index.html` in the browser.
- Use a local HTTP server from the frontend folder:
  ```powershell
  cd c:\CITYBUS\frontend
  python -m http.server 5500
  ```
- Then open `http://localhost:5500`.

### 8. Run FastAPI backend
From `c:\CITYBUS\backend` with the virtual environment active:
```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
- Verify at `http://localhost:8000/docs`.

### 9. Connect frontend to backend
- The frontend uses `frontend/js/app.js` to call backend endpoints.
- For local development, ensure `API_BASE` points to `http://localhost:8000`.
- In production, set `CORS_ORIGINS` and API host accordingly.

### 10. Debugging
- Backend: use VS Code launch configuration for Python and `uvicorn`.
- Frontend: open browser DevTools and check network requests.
- Check console errors for missing API responses or CORS failures.

## Part 2 — Supabase Setup

### 1. Create account
- Go to https://app.supabase.com and sign up.
- Confirm your email address.

### 2. Create a project
- Click `New project`.
- Choose a secure `Database password` and store it safely.
- Choose the nearest region for performance.

### 3. API keys and URL
- In Supabase, go to `Settings` → `API`.
- Copy the `Project URL` and `anon/public` key.
- Use these in `backend/.env` or your hosting environment variables.

### 4. Import SQL schema
- Go to Supabase SQL Editor.
- Paste the contents of `database/supabase_schema.sql`.
- Run the script.

### 5. Verify tables
- In the Supabase table browser, confirm tables are created:
  - `users`
  - `employees`
  - `roles`
  - `buses`
  - `routes`
  - `schedules`
  - `seats`
  - `bookings`
  - `booking_seats`
  - `payments`
  - `tickets`
  - `reports`
  - `finance_reports`
  - `refund_logs`
  - `audit_logs`

### 6. Auth settings
- Supabase Auth is optional for local API.
- This FastAPI backend uses JWT auth instead of Supabase Auth.

### 7. RLS basics
- Role-based access control is enforced in the backend.
- If using Supabase Auth tables, configure Row Level Security for extra protection.

### 8. Storage
- Static frontend assets are hosted outside Supabase.
- Use Supabase Storage only if you need file uploads for receipts, reports, or assets.

### 9. Testing
- Use Postman or browser to perform API login and booking flows.
- Confirm that role-based endpoints return HTTP 403 when unauthorized.

## Part 3 — Backend Deployment

### 1. Vercel limitations
- Vercel can host Python with the `@vercel/python` runtime.
- Vercel is not ideal for long-running stateful services and may have cold-start delay.
- For production, Render or Railway is recommended for a backend API.

### 2. Recommended host
- Render: good for Python FastAPI + PostgreSQL.
- Railway: also good for quick API deployment and database integration.
- Use Vercel only for frontend if backend needs a robust service.

### 3. Environment variables
In the hosting dashboard, set:
- `DATABASE_URL`
- `JWT_SECRET`
- `JWT_ALGORITHM=HS256`
- `JWT_EXP_MINUTES=60`
- `CORS_ORIGINS=https://your-frontend-url.com`

### 4. Secrets
- Never commit `.env` to Git.
- Use secret storage in Render/Railway/Vercel.

### 5. Production CORS
- Allow only trusted origins.
- Example: `https://yourdomain.com`.

### 6. Domain linking
- Configure custom domain in the hosting provider.
- Add DNS records as instructed by the provider.

### 7. API verification
- Confirm `https://api.yourdomain.com/docs` loads.
- Test key endpoints: `/auth/user/login`, `/bookings/reserve`, `/qr/validate`.

## Part 4 — Frontend + Domain Deployment

### 1. GitHub push
- Add the repo to GitHub.
- Commit all files and push to main branch.

### 2. Vercel import
- Create a new Vercel project.
- Connect GitHub repository.
- Set the root to the repository root for static frontend.
- Configure build as static if only frontend is deployed there.

### 3. Build settings
- For frontend-only deployment, no build command is required if files are static.
- Ensure `public` or `frontend` is served correctly.

### 4. Domain purchase
- Buy a domain from any registrar.
- Add it to Vercel or your hosting provider.

### 5. DNS
- Add the required A/CNAME records.
- Wait for DNS propagation.

### 6. SSL
- Most hosts provide automatic SSL.
- Confirm `https://yourdomain.com` is secure.

### 7. API integration
- Update frontend API base URL to your deployed backend.
- Use the correct production endpoints.

### 8. Final testing
- Test registration, login, booking, payment placeholder, and ticket pages.
- Test employee login and admin/operator/finance dashboards.

## Part 5 — GitHub Workflow

### 1. Repo creation
- Create a new GitHub repository.
- Push the full `c:\CITYBUS` project.

### 2. Commit
- Use meaningful commit messages.
- Example: `feat: add initial frontend and backend implementation`

### 3. Push
- Push to `main` or `master`.
- Use `git push origin main`.

### 4. Branching
- Create feature branches for enhancements.
- Example: `feature/employee-auth`, `feature/front-end-polish`.

### 5. Auto deployment
- Connect GitHub to Vercel/Render/Railway for automatic deployments.
- Set the deployment branch to `main`.

## Part 6 — Vercel Deployment

### 1. Vercel project setup
- Go to https://vercel.com and sign in.
- Create a new project and import your GitHub repository.
- Use the root of the repo as the project source.

### 2. Configure project files
- Confirm `vercel.json` is present in the repo root.
- Confirm `backend/requirements.txt` exists and `backend/main.py` is the FastAPI entrypoint.
- Confirm `frontend/index.html` is the static frontend entrypoint.

### 3. Vercel environment variables
In the Vercel dashboard, set these environment variables for production and preview:
- `DATABASE_URL` = your PostgreSQL connection string
- `JWT_SECRET` = a strong secret phrase
- `JWT_ALGORITHM` = `HS256`
- `JWT_EXP_MINUTES` = `60`
- `CORS_ORIGINS` = `https://your-vercel-domain.vercel.app`

### 4. Vercel routing behavior
- The backend API will be available at `https://<your-project>.vercel.app/api/...`.
- The frontend static site will be served from the same Vercel deployment.
- The default frontend base API path is `/api`, which matches the Vercel route.

### 5. Deploy and verify
- Deploy the project from the Vercel dashboard.
- Open the deployment URL.
- Confirm the API docs are available at `https://<your-project>.vercel.app/api/docs`.
- Test a simple endpoint like `/api/routes/list`.

### 6. Production testing
- Use the deployed URL in the frontend.
- Make sure the login and booking flows work.
- Confirm CORS errors do not appear in the browser console.
- If needed, add the exact Vercel production URL to `CORS_ORIGINS`.

## Troubleshooting
- If frontend cannot reach backend, check CORS settings.
- If login fails, verify `JWT_SECRET` and `DATABASE_URL`.
- If database imports fail, inspect the SQL syntax around the trigger definitions.

## Notes
- This document is intentionally separate from `README.md` per your request.
- Use `README.md` for the project overview and `DEPLOYMENT.md` for the detailed process.
