function InventoryTable({ inventories, onAdjustStock }) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>Batch</th>
            <th>Rack</th>
            <th>Quantity</th>
            <th style={{ textAlign: "right" }}>Actions</th>
          </tr>
        </thead>

        <tbody>
          {inventories.length === 0 ? (
            <tr>
              <td colSpan="5" style={{ textAlign: "center", color: "var(--text-secondary)", padding: "32px" }}>
                No inventories found.
              </td>
            </tr>
          ) : (
            inventories.map((inventory) => (
              <tr key={inventory.inventory_id}>
                <td>
                  <span style={{ fontWeight: 600 }}>{inventory.product_name}</span>
                </td>
                <td>
                  <span className="badge badge-slate">{inventory.batch_name}</span>
                </td>
                <td>
                  <span className="badge badge-violet">{inventory.rack_number}</span>
                </td>
                <td>
                  <span style={{ fontFamily: "monospace", fontSize: "15px", fontWeight: "bold" }}>
                    {inventory.quantity}
                  </span>
                </td>
                <td style={{ textAlign: "right" }}>
                  <button
                    className="btn btn-outline-violet btn-sm"
                    onClick={() => onAdjustStock(inventory)}
                  >
                    Adjust Stock
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default InventoryTable;