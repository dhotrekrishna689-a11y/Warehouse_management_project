const API_BASE_URL = "/api";

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.message || "Could not complete the supplier order request.");
  return payload.data;
}

export function getPendingSupplierOrders(supplierId) {
  return request(`/supplier/purchase-orders/pending?supplier_id=${encodeURIComponent(supplierId)}`);
}

export function getSupplierOrder(orderId) {
  return request(`/supplier/purchase-orders/${orderId}`);
}

export function prepareSupplierOrder(orderId, preparation) {
  return request(`/supplier/purchase-orders/${orderId}/prepare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(preparation),
  });
}

export function confirmSupplierOrder(orderId) {
  return request(`/supplier/purchase-orders/${orderId}/confirm`, { method: "POST" });
}
