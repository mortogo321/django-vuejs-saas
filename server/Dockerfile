# syntax=docker/dockerfile:1.7
#
# Django backend — multi-stage build.
#
# Stages:
#   1. base    — pinned python base, common env
#   2. builder — installs build toolchain + wheels into a venv
#   3. runtime — minimal image: venv + app, unprivileged user
#   4. dev     — runtime + postgres client (compose overrides CMD)

FROM python:3.14-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=60 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app

FROM base AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "$VIRTUAL_ENV" \
    && pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

FROM base AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
        tini \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 1001 app \
    && useradd --system --uid 1001 --gid app --home-dir /app --shell /usr/sbin/nologin app

COPY --from=builder /opt/venv /opt/venv

ARG APP_ENV=dev
ENV APP_ENV=${APP_ENV}

# Entrypoint comes from the named `infra` build context.
# Compose wires this with `additional_contexts: infra: ./docker/backend`.
COPY --from=infra --chown=app:app start.sh /app/start.sh
RUN chmod +x /app/start.sh

COPY --chown=app:app . /app

RUN cp /app/.env.${APP_ENV} /app/.env \
    && chown app:app /app/.env

RUN python manage.py collectstatic --noinput 2>/dev/null || true \
    && chown -R app:app /app

USER app
EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini", "--", "/app/start.sh"]

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=3 \
    CMD curl --fail --silent http://127.0.0.1:8000/api/health/ || exit 1

CMD ["gunicorn", "core.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--threads", "4", \
     "--timeout", "30", \
     "--graceful-timeout", "30", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

FROM runtime AS dev

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*
USER app
