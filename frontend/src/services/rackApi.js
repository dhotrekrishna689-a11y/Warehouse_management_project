const API_BASE_URL = "/api";

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.message || "The request could not be completed.");
  }

  return payload;
}

export async function getRacks() {
  const payload = await request("/racks");
  return payload.data || [];
}

export async function getRackUtilization() {
  const payload = await request("/racks/utilization");
  return payload.rack_utilization || [];
}

export async function createRack(rackCode, capacity) {
  return request("/racks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rack_code: rackCode, capacity: Number(capacity) }),
  });
}

export async function updateRack(rackId, rackCode) {
  return request(`/racks/${rackId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rack_code: rackCode }),
  });
}

export async function deleteRack(rackId) {
  return request(`/racks/${rackId}`, { method: "DELETE" });
}

export async function moveProduct(movement) {
  return request("/product-movements", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(movement),
  });
}

export async function getBatches() {
  const payload = await request("/batches");
  return payload.data || [];
}
