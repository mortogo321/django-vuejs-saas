# Django + Vue SaaS Starter

[![CI](https://github.com/mortogo321/django-vuejs-saas/actions/workflows/ci.yml/badge.svg)](https://github.com/mortogo321/django-vuejs-saas/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](server/requirements.txt)
[![Django 5.2 LTS](https://img.shields.io/badge/django-5.2_LTS-092E20.svg)](server/requirements.txt)
[![Vue 3](https://img.shields.io/badge/vue-3-4FC08D.svg)](frontend/package.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A minimal multi-tenant SaaS starter: Django REST backend (custom per-user
`Profile` with team association, admin, OpenAPI schema) plus a Vue 3 +
Vite + TypeScript frontend that renders the API health state. Early-stage
scaffold — billing, team management, and tenant scoping are intentionally
left as extension points.

## What's inside

- `server/core` — env-driven Django settings, URL routing, WSGI/ASGI entry points
- `server/base` — landing page + `GET /api/health/` probe (JSON `{"status": "ok"}`)
- `server/user` — `Profile` model (`OneToOne` to `User` + `active_team_id`), admin, tests
- `server` — DRF + `drf-spectacular` schema at `/api/schema/`, Swagger UI at `/api/docs/`
- `frontend` — Vue 3 + Vite + TS app (bun-first) showing live API health
- `docker/` — backend entrypoint, nginx reverse proxy (frontend + `/api` + `/admin`)
- `.github/workflows/ci.yml` — quality (Ruff + Biome + typecheck) → tests → Docker builds

## Tech stack

| Layer | Choice |
|---|---|
| Backend | Python 3.13, Django 5.2 LTS, DRF 3.18, django-filter, drf-spectacular |
| Data | PostgreSQL 17 (prod/compose) with SQLite fallback for local dev, Redis 8 cache |
| Server | Gunicorn 26, WhiteNoise static, nginx 1.29 reverse proxy |
| Frontend | Vue 3.5, Vite 8, TypeScript 5.9 strict, Vitest 5, Biome 2.5, Bun 1.4 |
| Quality | Ruff (lint+format), Biome (lint+format), vue-tsc, pytest + pytest-django |
| Ops | Multi-stage Docker (pinned, non-root, HEALTHCHECK), Compose dev/uat/prod, Dependabot weekly |

## Quickstart

Backend (SQLite, no Docker):

```bash
cd server
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend (needs the backend on `:8000`):

```bash
cd frontend
bun install
bun run dev
```

Docker (Postgres 17 + Redis 8 + backend + frontend):

```bash
docker compose up --build
```

The app serves the landing page at `http://localhost:8000/`, the Vue dev
server at `http://localhost:5173/`, the health probe at
`http://localhost:8000/api/health/`, Swagger at
`http://localhost:8000/api/docs/`, and the Django admin at
`http://localhost:8000/admin/`.

## Configuration

| Variable | Default (dev) | Notes |
|---|---|---|
| `DEBUG` | `True` | Set `False` in uat/prod |
| `DJANGO_SECRET_KEY` | dev-only insecure | **Required** when `DEBUG=False` (fail-fast) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | **Required** when `DEBUG=False` |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Explicit allowlist, never `*` + credentials |
| `POSTGRES_HOST` | unset (SQLite) | Set to `db` under compose for PostgreSQL 17 |
| `POSTGRES_DB/USER/PASSWORD/PORT` | `saas/saas/saas_dev/5432` | Injected per environment |
| `REDIS_URL` | unset (locmem) | `redis://redis:6379/0` under compose |
| `VITE_API_URL` | `/api` (Vite proxy) | `http://localhost:8000/api` in dev compose |

Per-environment committed defaults live in `server/.env.dev`,
`server/.env.uat`, and `server/.env.prod`. Production secrets are injected
at deploy time — never baked into the image. The Docker build stamps
`.env.<APP_ENV>` as `.env` via `APP_ENV` build arg.

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Server-rendered Bootstrap landing page |
| `GET` | `/api/health/` | Liveness probe → `{"status": "ok"}` |
| `GET` | `/api/schema/` | OpenAPI 3 schema (JSON) |
| `GET` | `/api/docs/` | Swagger UI |
| `GET` | `/admin/` | Django admin (Profile registered) |

## Tests

```bash
cd server && pytest -q        # 14 tests: landing, health, Profile model
cd frontend && bun run test   # 6 tests: health-URL helpers + fetchHealth
```

Quality gates (same as CI):

```bash
cd server && ruff check . && ruff format --check . && pytest -q
cd frontend && bun run ci:check && bun run typecheck && bun run test
```

## Structure

```
server/
├── core/          # settings (env-driven), urls, wsgi/asgi
├── base/          # landing view + /api/health/, templates
├── user/          # Profile model (OneToOne) + admin + tests
├── requirements.txt  # pinned majors
├── pyproject.toml    # ruff + pytest config
├── Dockerfile        # base/builder/runtime/dev, non-root + HEALTHCHECK
└── .env.{dev,uat,prod}
frontend/
├── src/           # App.vue + api/health.ts client
├── tests/         # vitest suite (no DOM needed)
├── vite.config.ts # /api → backend:8000 proxy
└── Dockerfile     # bun deps/dev/build + nginx production
docker/
├── backend/start.sh  # wait-for-db → migrate → collectstatic → exec CMD
└── nginx/            # reverse proxy: / → SPA, /api|/admin → backend
```

## Security notes

- `SECRET_KEY` and `ALLOWED_HOSTS` fail fast when `DEBUG=False` without real values.
- CORS uses an explicit origin list; credentials are only enabled when origins exist.
- Production sets `SECURE_SSL_REDIRECT`, HSTS, and secure session/CSRF cookies.
- Runtime images run as non-root `app` with `tini` as PID 1 and `curl` healthchecks.
- Dependabot watches pip, npm, Docker, and GitHub Actions weekly.

## License

MIT — see [LICENSE](LICENSE).
