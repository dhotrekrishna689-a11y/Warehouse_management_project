const API_BASE_URL = "/api";

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.message || "Request failed.");
  return payload;
}

export async function getInboundRacks() {
  const payload = await request("/racks");
  return payload.data || [];
}

export async function receiveShipment(shipment) {
  return request("/shipments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(shipment),
  });
}
