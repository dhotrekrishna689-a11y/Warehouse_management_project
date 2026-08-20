const API_BASE_URL = "/api";

export async function getOrders() {
  const response = await fetch(`${API_BASE_URL}/orders`);
  if (!response.ok) {
    throw new Error("Failed to fetch orders");
  }
  const data = await response.json();
  return data.data;
}

export async function createOrder(orderData) {
  const response = await fetch(`${API_BASE_URL}/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(orderData),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || "Failed to create order");
  }

  return await response.json();
}

export async function getPickList(orderId) {
  const response = await fetch(`${API_BASE_URL}/orders/${orderId}/pick-list`);
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    if (response.status === 400 && data.message) {
      return data;
    }
    throw new Error(data.message || "Failed to fetch pick list");
  }
  return data;
}

export async function updateInventoryAfterPick(orderId, items) {
  const response = await fetch(`${API_BASE_URL}/orders/${orderId}/update-inventory`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ items }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || "Failed to update inventory after pick");
  }

  return await response.json();
}
