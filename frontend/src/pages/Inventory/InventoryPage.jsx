import InventoryTable from "../../components/inventory/InventoryTable";

function InventoryPage() {
  const inventories = [
    {
      inventory_id: 13,
      product_name: "Potato",
      batch_name: "BATCH-POT-001",
      rack_number: "C1",
      quantity: 200,
    },
    {
      inventory_id: 14,
      product_name: "Rice",
      batch_name: "BATCH-RIC-001",
      rack_number: "A2",
      quantity: 150,
    },
  ];

  return (
    <div>
      <h1>Inventory</h1>

      <InventoryTable inventories={inventories} />
    </div>
  );
}

export default InventoryPage;