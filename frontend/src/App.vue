<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { fetchHealth, isHealthy } from "./api/health";

const apiStatus = ref<string>("checking…");
const apiOk = ref<boolean>(false);
let controller: AbortController | null = null;

onMounted(async () => {
  controller = new AbortController();
  try {
    const payload = await fetchHealth(controller.signal);
    apiOk.value = isHealthy(payload);
    apiStatus.value = apiOk.value ? "ok" : `unexpected: ${payload.status}`;
  } catch (error) {
    apiOk.value = false;
    apiStatus.value = error instanceof Error ? error.message : "unreachable";
  }
});

onUnmounted(() => {
  controller?.abort();
  controller = null;
});
</script>

<template>
  <main class="page">
    <section class="card">
      <p class="eyebrow">Django + Vue SaaS starter</p>
      <h1>Multi-tenant SaaS scaffold</h1>
      <p class="lede">
        Django REST backend with a Vue 3 frontend. The backend serves the API at
        <code>/api</code> and a health probe at <code>/api/health/</code>.
      </p>
      <p class="status" :data-ok="apiOk">
        <span class="dot" aria-hidden="true"></span>
        API status: <strong>{{ apiStatus }}</strong>
      </p>
      <ul class="links">
        <li><a href="/api/health/">Health JSON</a></li>
        <li><a href="/api/docs/">API docs (Swagger)</a></li>
        <li><a href="/admin/">Django admin</a></li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 2rem 1rem;
  background: #0f172a;
  color: #e2e8f0;
  font-family: ui-sans-serif, system-ui, sans-serif;
}
.card {
  max-width: 36rem;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 1rem;
  padding: 2rem;
}
.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0 0 0.5rem;
}
h1 {
  margin: 0 0 0.75rem;
  font-size: 1.75rem;
}
.lede {
  color: #cbd5e1;
  line-height: 1.6;
}
code {
  background: #0f172a;
  padding: 0.1rem 0.35rem;
  border-radius: 0.375rem;
}
.status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.dot {
  width: 0.65rem;
  height: 0.65rem;
  border-radius: 9999px;
  background: #f59e0b;
}
.status[data-ok="true"] .dot {
  background: #22c55e;
}
.links {
  display: flex;
  gap: 1rem;
  padding: 0;
  list-style: none;
  margin: 1rem 0 0;
}
.links a {
  color: #93c5fd;
}
</style>
