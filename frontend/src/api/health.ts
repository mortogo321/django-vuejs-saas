export interface HealthResponse {
  status: string;
}

const API_BASE: string =
  (import.meta.env.VITE_API_URL as string | undefined) ?? "/api";

export function healthUrl(): string {
  return `${API_BASE.replace(/\/$/, "")}/health/`;
}

export async function fetchHealth(
  signal?: AbortSignal,
): Promise<HealthResponse> {
  const response = await fetch(healthUrl(), { signal });
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  const data = (await response.json()) as unknown;
  if (typeof data !== "object" || data === null || !("status" in data)) {
    throw new Error("Health check returned an unexpected payload");
  }
  return { status: String((data as { status: unknown }).status) };
}

export function isHealthy(payload: HealthResponse): boolean {
  return payload.status === "ok";
}
