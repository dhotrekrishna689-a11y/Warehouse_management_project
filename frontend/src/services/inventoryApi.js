const API_BASE_URL = "/api";

export async function getInventories() {
    const response = await fetch(`${API_BASE_URL}/inventories`);

    if (!response.ok) {
        throw new Error("Failed to fetch inventories");
    }

    const data = await response.json();
    return data.data;
}

export async function adjustStock(inventoryId, quantity, reason) {
    const response = await fetch(`${API_BASE_URL}/inventories/${inventoryId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity: Number(quantity), reason }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || "Failed to adjust stock");
    }

    return await response.json();
}