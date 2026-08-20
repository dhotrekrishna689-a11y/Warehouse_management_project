import { useState } from "react";

function CreateOrderModal({ products, onClose, onSubmit }) {
  const [customerName, setCustomerName] = useState("");
  const [orderDate, setOrderDate] = useState(new Date().toISOString().split("T")[0]);
  const [items, setItems] = useState([{ product_id: "", quantity: 1 }]);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAddItem = () => {
    setItems([...items, { product_id: "", quantity: 1 }]);
  };

  const handleRemoveItem = (index) => {
    if (items.length === 1) return;
    setItems(items.filter((_, i) => i !== index));
  };

  const handleItemChange = (index, field, value) => {
    const updated = [...items];
    updated[index][field] = value;
    setItems(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!customerName.trim()) {
      setError("Customer name is required.");
      return;
    }
    if (!orderDate) {
      setError("Order date is required.");
      return;
    }
    for (let i = 0; i < items.length; i++) {
      if (!items[i].product_id) {
        setError(`Please select a product for item #${i + 1}.`);
        return;
      }
      if (!items[i].quantity || items[i].quantity <= 0) {
        setError(`Please enter a valid quantity for item #${i + 1}.`);
        return;
      }
    }

    setIsSubmitting(true);
    setError("");

    try {
      const payload = {
        customer_name: customerName,
        order_date: orderDate,
        items: items.map(item => ({
          product_id: Number(item.product_id),
          quantity: Number(item.quantity)
        }))
      };
      await onSubmit(payload);
    } catch (err) {
      setError(err.message || "Failed to create order.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" style={{ maxWidth: "600px" }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Create New Customer Order</h3>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && (
              <div style={{ color: "var(--danger-color)", fontSize: "14px", padding: "10px", background: "rgba(239, 68, 68, 0.1)", borderRadius: "var(--radius-sm)", border: "1px solid rgba(239, 68, 68, 0.2)" }}>
                {error}
              </div>
            )}

            <div className="form-group">
              <label>Customer Name</label>
              <input 
                type="text" 
                placeholder="e.g. Acme Corporation" 
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Order Date</label>
              <input 
                type="date" 
                value={orderDate}
                onChange={(e) => setOrderDate(e.target.value)}
                required
              />
            </div>

            <div style={{ marginTop: "12px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <label style={{ fontSize: "13px", fontWeight: "600", color: "var(--text-secondary)" }}>Order Items</label>
                <button type="button" className="btn btn-secondary btn-sm" onClick={handleAddItem}>
                  + Add Product Item
                </button>
              </div>

              {items.map((item, idx) => (
                <div key={idx} style={{ display: "flex", gap: "12px", marginBottom: "12px", alignItems: "center" }}>
                  <div className="form-group" style={{ flex: 2 }}>
                    <select
                      value={item.product_id}
                      onChange={(e) => handleItemChange(idx, "product_id", e.target.value)}
                      required
                    >
                      <option value="">Select Product...</option>
                      {products.map((p) => (
                        <option key={p.product_id} value={p.product_id}>
                          {p.name} {p.sku ? `(${p.sku})` : ""}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group" style={{ flex: 1 }}>
                    <input
                      type="number"
                      min="1"
                      placeholder="Qty"
                      value={item.quantity}
                      onChange={(e) => handleItemChange(idx, "quantity", e.target.value)}
                      required
                    />
                  </div>

                  {items.length > 1 && (
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      style={{ color: "var(--danger-color)", height: "42px" }}
                      onClick={() => handleRemoveItem(idx)}
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
              {isSubmitting ? "Creating..." : "Create Order"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateOrderModal;
