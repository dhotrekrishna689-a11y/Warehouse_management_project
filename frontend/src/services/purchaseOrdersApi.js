const API_BASE_URL = "/api";

export async function placePurchaseOrder(supplierId, items) {
  const response = await fetch(`${API_BASE_URL}/po/Purchase-order`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ supplier_id: Number(supplierId), items: items.map(({ product_id, quantity }) => ({ product_id: Number(product_id), quantity: Number(quantity) })) }),
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.message || "Could not place the supplier order.");
  return payload;
}
