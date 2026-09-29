# syntax=docker/dockerfile:1.7
#
# Vue frontend — multi-stage build.
#   deps ....... install with bun (cached)
#   dev ........ vite dev server with hot reload
#   builder .... production `vite build` output in /app/dist
#   production . nginx serving /usr/share/nginx/html + /api/health proxy

ARG BUN_VERSION=1.4.2
ARG NODE_VERSION=26.10-alpine
ARG NGINX_VERSION=1.29-alpine

FROM oven/bun:${BUN_VERSION}-alpine AS deps
WORKDIR /app
COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile 2>/dev/null || bun install

FROM deps AS dev
COPY . .
EXPOSE 5173
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=3 \
  CMD bun --version || exit 1
CMD ["bun", "run", "dev", "--host", "0.0.0.0", "--port", "5173"]

FROM deps AS builder
COPY . .
RUN bun run build

FROM nginx:${NGINX_VERSION} AS production
COPY --from=nginx nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist /usr/share/nginx/html
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/ || exit 1
EXPOSE 80
