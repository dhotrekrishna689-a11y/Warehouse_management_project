function OrderTable({ orders, onViewPickList }) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Order Number</th>
            <th>Customer Name</th>
            <th>Order Date</th>
            <th>Status</th>
            <th style={{ textAlign: "right" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.length === 0 ? (
            <tr>
              <td colSpan="5" style={{ textAlign: "center", color: "var(--text-secondary)", padding: "32px" }}>
                No orders found. Click "+ Create Order" to add one.
              </td>
            </tr>
          ) : (
            orders.map((order) => {
              const isDispatched = order.status === "DISPATCHED";
              return (
                <tr key={order.order_id}>
                  <td>
                    <span className="badge badge-violet" style={{ fontSize: "13px" }}>
                      {order.order_number || `ORD-${String(order.order_id).padStart(6, '0')}`}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontWeight: 600 }}>{order.customer_name}</span>
                  </td>
                  <td>
                    <span style={{ color: "var(--text-secondary)" }}>{order.order_date}</span>
                  </td>
                  <td>
                    <span 
                      className={`badge ${isDispatched ? 'badge-slate' : 'badge-violet'}`}
                      style={{ 
                        background: isDispatched ? "rgba(16, 185, 129, 0.15)" : "rgba(245, 158, 11, 0.15)",
                        color: isDispatched ? "#10b981" : "#f59e0b",
                        border: isDispatched ? "1px solid rgba(16, 185, 129, 0.3)" : "1px solid rgba(245, 158, 11, 0.3)"
                      }}
                    >
                      {order.status || "PENDING"}
                    </span>
                  </td>
                  <td style={{ textAlign: "right" }}>
                    <button
                      className={`btn btn-sm ${isDispatched ? 'btn-secondary' : 'btn-outline-violet'}`}
                      onClick={() => onViewPickList(order)}
                      disabled={isDispatched}
                      style={{ opacity: isDispatched ? 0.7 : 1, cursor: isDispatched ? "not-allowed" : "pointer" }}
                    >
                      {isDispatched ? "Dispatched ✅" : "View Pick List"}
                    </button>
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}

export default OrderTable;
