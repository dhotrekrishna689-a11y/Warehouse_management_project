function InventoryTable({ inventories }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Product</th>
          <th>Batch</th>
          <th>Rack</th>
          <th>Quantity</th>
        </tr>
      </thead>

      <tbody>
        {inventories.map((inventory) => (
          <tr key={inventory.inventory_id}>
            <td>{inventory.product_name}</td>
            <td>{inventory.batch_name}</td>
            <td>{inventory.rack_number}</td>
            <td>{inventory.quantity}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default InventoryTable;