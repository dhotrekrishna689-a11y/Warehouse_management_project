import { useState } from "react";

function PickListModal({ pickListData, onClose, onConfirmDispatch }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  if (!pickListData) return null;

  // Handle case where backend returns insufficient stock error object
  const isErrorResponse = pickListData.message && !pickListData.items;

  const handleConfirm = async () => {
    setIsSubmitting(true);
    setError("");
    setSuccessMsg("");

    try {
      // Map pick_list items to payload expected by update_inventory_after_pick
      const itemsPayload = pickListData.items.map(item => ({
        inventory_id: item.inventory_id,
        quantity: item.pick_quantity
      }));

      await onConfirmDispatch(pickListData.order_id, itemsPayload);
      setSuccessMsg("Inventory successfully updated and items dispatched!");
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (err) {
      setError(err.message || "Failed to confirm dispatch.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" style={{ maxWidth: "650px" }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>FEFO Pick List - {pickListData.order_number || `Order #${pickListData.order_id}`}</h3>
          <p style={{ fontSize: "13px", color: "var(--text-secondary)", marginTop: "4px" }}>
            Customer: <strong style={{ color: "var(--text-primary)" }}>{pickListData.customer_name}</strong>
          </p>
        </div>

        <div className="modal-body">
          {error && (
            <div style={{ color: "var(--danger-color)", fontSize: "14px", padding: "10px", background: "rgba(239, 68, 68, 0.1)", borderRadius: "var(--radius-sm)", border: "1px solid rgba(239, 68, 68, 0.2)" }}>
              {error}
            </div>
          )}

          {successMsg && (
            <div style={{ color: "var(--success-color)", fontSize: "14px", padding: "10px", background: "rgba(16, 185, 129, 0.1)", borderRadius: "var(--radius-sm)", border: "1px solid rgba(16, 185, 129, 0.2)" }}>
              {successMsg}
            </div>
          )}

          {isErrorResponse ? (
            <div 
              style={{ 
                padding: "24px", 
                textAlign: "center", 
                color: pickListData.status === "OUT_OF_STOCK" ? "var(--danger-color)" : "var(--warning-color)", 
                background: pickListData.status === "OUT_OF_STOCK" ? "rgba(239, 68, 68, 0.08)" : "rgba(245, 158, 11, 0.08)", 
                borderRadius: "var(--radius-md)", 
                border: pickListData.status === "OUT_OF_STOCK" ? "1px solid rgba(239, 68, 68, 0.2)" : "1px solid rgba(245, 158, 11, 0.2)" 
              }}
            >
              <div style={{ fontSize: "16px", fontWeight: "600", marginBottom: "6px" }}>
                {pickListData.status === "OUT_OF_STOCK" ? "⚠️ Insufficient Warehouse Stock" : "✅ Order Already Dispatched"}
              </div>
              <div style={{ fontSize: "13px", color: "var(--text-secondary)" }}>
                {pickListData.message}
              </div>
            </div>
          ) : (
            <div className="table-container" style={{ marginTop: "0" }}>
              <table>
                <thead>
                  <tr>
                    <th>Product ID</th>
                    <th>Batch ID</th>
                    <th>Rack Location</th>
                    <th>Pick Quantity</th>
                  </tr>
                </thead>
                <tbody>
                  {pickListData.items && pickListData.items.length > 0 ? (
                    pickListData.items.map((item, idx) => (
                      <tr key={idx}>
                        <td>
                          <span style={{ fontWeight: "600" }}>Product #{item.product_id}</span>
                        </td>
                        <td>
                          <span className="badge badge-slate">Batch #{item.batch_id}</span>
                        </td>
                        <td>
                          <span className="badge badge-violet">Rack #{item.rack_id}</span>
                        </td>
                        <td>
                          <span style={{ fontFamily: "monospace", fontSize: "15px", fontWeight: "bold", color: "var(--success-color)" }}>
                            {item.pick_quantity} units
                          </span>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="4" style={{ textAlign: "center", color: "var(--text-secondary)" }}>
                        No pick items found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button type="button" className="btn btn-secondary" onClick={onClose} disabled={isSubmitting}>
            Close
          </button>
          {!isErrorResponse && pickListData.items && pickListData.items.length > 0 && (
            <button 
              type="button" 
              className="btn btn-primary" 
              onClick={handleConfirm}
              disabled={isSubmitting || !!successMsg}
            >
              {isSubmitting ? "Dispatching..." : "Confirm Dispatch & Deduct Stock"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default PickListModal;
