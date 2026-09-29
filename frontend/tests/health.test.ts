import { afterEach, describe, expect, it, vi } from "vitest";
import { fetchHealth, healthUrl, isHealthy } from "../src/api/health";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe("healthUrl", () => {
  it("points at the /health/ probe", () => {
    expect(healthUrl().endsWith("/health/")).toBe(true);
  });
});

describe("isHealthy", () => {
  it("accepts status ok", () => {
    expect(isHealthy({ status: "ok" })).toBe(true);
  });

  it("rejects anything else", () => {
    expect(isHealthy({ status: "degraded" })).toBe(false);
    expect(isHealthy({ status: "" })).toBe(false);
  });
});

describe("fetchHealth", () => {
  it("returns the parsed payload on 200", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({ ok: true, json: async () => ({ status: "ok" }) })),
    );
    await expect(fetchHealth()).resolves.toEqual({ status: "ok" });
  });

  it("throws on non-2xx", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({ ok: false, status: 500, json: async () => ({}) })),
    );
    await expect(fetchHealth()).rejects.toThrow("Health check failed: 500");
  });

  it("throws on malformed payloads", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({ ok: true, json: async () => ({ hello: 1 }) })),
    );
    await expect(fetchHealth()).rejects.toThrow("unexpected payload");
  });
});
