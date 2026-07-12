# Django SaaS Starter (Backend)

A minimal Django backend scaffold demonstrating project/app structure for a multi-tenant SaaS-style application, including a custom user-profile model with team association.

## What's inside

- `core` — Django project configuration (settings, URL routing, WSGI/ASGI entry points)
- `base` — landing page app: a single view rendering a Bootstrap-based welcome page, with header/footer/dark-mode template partials
- `user` — a `Profile` model extending Django's built-in `User` with an `active_team_id` field, laid out for future multi-tenant/team-scoped features
- Django admin enabled for both apps

This is an early-stage backend scaffold. There is no frontend application in this repository (the default landing page uses server-rendered templates styled with Bootstrap via CDN); SaaS features such as billing, team management, or an API are not yet implemented.

## Tech stack

- Python, Django 5.x
- SQLite (default development database)
- Django templates + Bootstrap 5 (CDN) for the sample landing page

## Quickstart

```bash
cd server
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The app serves the landing page at `http://localhost:8000/` and the Django admin at `http://localhost:8000/admin/`.

## Structure

```
server/
├── core/    # project settings, URL config, WSGI/ASGI
├── base/    # landing page view + templates
└── user/    # Profile model (user ↔ team association)
```
