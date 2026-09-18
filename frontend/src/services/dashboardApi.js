const BASE = "/api";

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || "Request failed");
  return data;
}

export async function getDashboard() {
  return get("/dashboard");
}