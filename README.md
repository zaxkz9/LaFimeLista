# Student Binnacle

A multi-user log ("binnacle") of homeworks and bills, built with Flask + PostgreSQL and server-rendered HTML/CSS.

## Stack

- **Backend:** Python 3, Flask (app factory + blueprints)
- **Database:** PostgreSQL via Flask-SQLAlchemy, migrations via Flask-Migrate
- **Auth:** Flask-Login, multi-user, each user's homeworks/bills are private to them
- **Frontend:** server-rendered Jinja2 templates, plain HTML/CSS (no JS framework)

## Project layout

```
app/
  models/       User, Category, Homework, Bill
  auth/         register, login, logout
  homeworks/    CRUD, filter by status/category
  bills/        CRUD, filter by status/category
  main/         dashboard (overdue / due-soon summary)
  templates/, static/
config.py       Dev/Prod/Test config, reads from environment
run.py          entry point
```

## Setup

1. Create a virtualenv and install dependencies:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and adjust `SECRET_KEY` / `DATABASE_URL` if needed.

3. Start Postgres (via Docker, or point `DATABASE_URL` at an existing instance):

   ```
   docker compose up -d
   ```

4. Run database migrations:

   ```
   flask db init
   flask db migrate -m "initial"
   flask db upgrade
   ```

5. Run the app:

   ```
   flask run
   ```

   Visit http://127.0.0.1:5000, register an account, and start logging homeworks and bills.

## Notes on scalability

- New feature areas (e.g. a JSON API, notifications) can be added as new blueprints without touching existing ones.
- Schema changes go through Flask-Migrate (`flask db migrate` / `upgrade`) instead of manual DB edits.
- All config (secret key, DB URL) comes from environment variables, so moving from a class project to a personal/public deployment is a config change, not a rewrite.
- Due-soon/overdue logic lives on the models (`Homework.is_overdue`, `is_due_soon()`, same on `Bill`); a real notification system (email/push) could hook into these later via a scheduler (e.g. APScheduler or Celery) without changing the data model.
