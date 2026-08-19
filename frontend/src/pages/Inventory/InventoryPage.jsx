import { useEffect, useState } from "react";
import InventoryTable from "../../components/inventory/InventoryTable";
import { getInventories, adjustStock } from "../../services/inventoryApi";

function InventoryPage() {
  const [inventories, setInventories] = useState([]);
  const [selectedInventory, setSelectedInventory] = useState(null);
  const [newQuantity, setNewQuantity] = useState("");
  const [reason, setReason] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchInventories = () => {
    getInventories()
      .then((data) => {
        setInventories(data);
      })
      .catch((error) => {
        console.error("Failed to load inventories:", error);
      });
  };

  useEffect(() => {
    fetchInventories();
  }, []);

  const handleOpenAdjustModal = (inventory) => {
    setSelectedInventory(inventory);
    setNewQuantity(inventory.quantity);
    setReason("");
    setError("");
  };

  const handleCloseModal = () => {
    setSelectedInventory(null);
  };

  const handleAdjustSubmit = async (e) => {
    e.preventDefault();
    if (!newQuantity || newQuantity < 0) {
      setError("Please enter a valid non-negative quantity.");
      return;
    }
    if (!reason.trim()) {
      setError("Please provide a reason for the adjustment.");
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      await adjustStock(selectedInventory.inventory_id, newQuantity, reason);
      fetchInventories();
      handleCloseModal();
    } catch (err) {
      setError(err.message || "Failed to adjust stock. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <h1>Inventory</h1>

      <InventoryTable 
        inventories={inventories} 
        onAdjustStock={handleOpenAdjustModal} 
      />

      {/* Adjust Stock Modal */}
      {selectedInventory && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Adjust Stock Level</h3>
            </div>
            
            <form onSubmit={handleAdjustSubmit}>
              <div className="modal-body">
                {error && (
                  <div style={{ color: "var(--danger-color)", fontSize: "14px", padding: "10px", background: "rgba(239, 68, 68, 0.1)", borderRadius: "var(--radius-sm)", border: "1px solid rgba(239, 68, 68, 0.2)" }}>
                    {error}
                  </div>
                )}
                
                <div className="form-group">
                  <label>Product</label>
                  <input 
                    type="text" 
                    value={selectedInventory.product_name} 
                    disabled 
                  />
                </div>

                <div className="form-group">
                  <label>Batch</label>
                  <input 
                    type="text" 
                    value={selectedInventory.batch_name} 
                    disabled 
                  />
                </div>

                <div className="form-group">
                  <label>Current Quantity</label>
                  <input 
                    type="text" 
                    value={selectedInventory.quantity} 
                    disabled 
                  />
                </div>

                <div className="form-group">
                  <label>New Quantity</label>
                  <input 
                    type="number" 
                    min="0"
                    placeholder="Enter new quantity"
                    value={newQuantity} 
                    onChange={(e) => setNewQuantity(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Reason for Adjustment</label>
                  <textarea 
                    placeholder="e.g. Damaged goods, count mismatch correction"
                    rows="3"
                    value={reason} 
                    onChange={(e) => setReason(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="modal-footer">
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={handleCloseModal}
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Updating..." : "Save Changes"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default InventoryPage;