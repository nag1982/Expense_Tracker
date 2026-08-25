# Ledgerly Expense Tracker

A focused Flask expense tracker with authentication, transaction management, budgets, dashboard totals, search, and reports.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

Open http://127.0.0.1:5000. The app uses a local SQLite database by default. Set `DATABASE_PATH` and `SECRET_KEY` in the environment for a different location and production secret.

## Test

```powershell
pytest
```

The included `vercel.json` provides a starting point for Vercel's Python runtime. For production, use a managed PostgreSQL adapter and configure migrations and environment variables in the deployment pipeline.
