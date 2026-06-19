# Employee Management Tool

A simple employee management web app built with Django. It covers authentication, employee CRUD, daily attendance (check-in/check-out), attendance reports, server-side pagination & search, data export (Excel/CSV), and an admin dashboard with charts.

## Features

- **Authentication**: Admin and Employee accounts, each redirected to a different home page after login.
- **Employee management (CRUD)**: admin can add, edit, and delete employee records (name, email, position, join date, active status).
- **Attendance**: employees can check in and check out once per day. Admin can see attendance for everyone, employees only see their own.
- **Pagination & search**: both the employee list and attendance report are paginated and searchable, all handled on the backend (no client-side JS filtering).
- **Export**: employee and attendance data can be exported to Excel (openpyxl) and CSV.
- **Dashboard**: `/dashboard/`, admin-only, shows employee count per position and a 7-day attendance chart using Chart.js.
- **REST API**: basic DRF endpoints at `/api/employees/` and `/api/attendance/` (mainly for completeness / testing with tools like Postman).

## Tech stack

- Django 4.2 (LTS)
- Django REST Framework
- SQLite
- openpyxl for Excel export, built-in `csv` module for CSV export
- Bootstrap 5 + Chart.js (via CDN, no frontend build step needed)

## Project layout

```
empman/        project settings & root urls
accounts/      custom User model (role: admin/employee), login/logout
employees/     Employee model, CRUD views, forms, exports, API
attendance/    Attendance model, check-in/out, report, exports, API
dashboard/     admin dashboard with charts
core/          shared permission mixins
templates/     all HTML templates
```

## Setup (local)

1. Clone the repo and go into the project folder.
2. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Load demo data (creates one admin account and 5 employee accounts with some
   attendance history for the past week):
   ```
   python manage.py seed_demo_data
   ```
6. Start the server:
   ```
   python manage.py runserver
   ```
7. Open `http://127.0.0.1:8000/` in your browser.

## Setup (Docker)

If you'd rather skip the virtualenv dance:

```
docker compose up --build
```

This builds the image, runs migrations, loads the demo data, and starts the
server at `http://127.0.0.1:8000/`. The SQLite file lives in a named volume
(`sqlite_data`) so your data survives `docker compose down` / restarts — only
`docker compose down -v` wipes it.

## Deploying (Render)

The repo includes a `render.yaml` blueprint, so deployment is mostly point-and-click:

1. Push the repo to GitHub (already done if you're reading this from there).
2. On [Render](https://render.com), go to **New > Blueprint**, connect this repo, and
   Render will read `render.yaml` and set everything up — build command, start
   command, and a generated `SECRET_KEY` — automatically.
3. Once it's live, demo data (the admin + 5 employee accounts) gets (re)created on
   every boot via `seed_demo_data`, so it's always there even after the service
   spins down on the free tier.

Note: Render's free web service tier doesn't have persistent disk, so the SQLite
file resets whenever the service restarts/redeploys. That's fine for demo purposes
since the seed step always restores the same accounts and sample attendance — just
don't expect manually-added data to survive a restart on the free tier.

## Demo credentials

| Role     | Username | Password    |
|----------|----------|-------------|
| Admin    | admin    | admin12345  |
| Employee | angel    | password123 |
| Employee | rizki    | password123 |
| Employee | siti     | password123 |
| Employee | bagus    | password123 |
| Employee | putri    | password123 |

## Notes

- Admin status is based on a `role` field on the custom User model (not just `is_staff`), so it's easy to tell apart from Django's built-in admin flag.
- Attendance records are unique per employee per day — checking in twice on the same day just updates the existing record instead of creating duplicates.
- The dashboard charts are rendered with Chart.js loaded from a CDN, fed by data computed with Django's ORM (`Count`, `annotate`) — no raw SQL anywhere in the app.
- Export and dashboard routes are guarded at the view level, so a regular employee hitting those URLs directly gets a 403, not just a hidden link.
