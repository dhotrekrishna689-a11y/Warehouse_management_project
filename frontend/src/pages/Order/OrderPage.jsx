import { useEffect, useState } from "react";
import OrderTable from "../../components/order/OrderTable";
import CreateOrderModal from "../../components/order/CreateOrderModal";
import PickListModal from "../../components/order/PickListModal";
import { getOrders, createOrder, getPickList, updateInventoryAfterPick } from "../../services/ordersApi";
import { getProducts } from "../../services/productsApi";

function OrderPage() {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [activePickList, setActivePickList] = useState(null);
  const [error, setError] = useState("");

  const loadData = async () => {
    try {
      const ordersData = await getOrders();
      setOrders(ordersData);
    } catch (err) {
      console.error("Error loading orders:", err);
    }

    try {
      const productsData = await getProducts();
      setProducts(productsData);
    } catch (err) {
      console.error("Error loading products:", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateOrderSubmit = async (orderData) => {
    await createOrder(orderData);
    await loadData();
    setIsCreateModalOpen(false);
  };

  const handleViewPickList = async (order) => {
    setError("");
    try {
      const pickListData = await getPickList(order.order_id);
      setActivePickList(pickListData);
    } catch (err) {
      setError(err.message || "Failed to load pick list for order.");
    }
  };

  const handleConfirmDispatch = async (orderId, items) => {
    await updateInventoryAfterPick(orderId, items);
    await loadData();
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <h1>Customer Orders</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setIsCreateModalOpen(true)}
        >
          + Create New Order
        </button>
      </div>

      {error && (
        <div style={{ color: "var(--danger-color)", fontSize: "14px", padding: "12px", background: "rgba(239, 68, 68, 0.1)", borderRadius: "var(--radius-md)", border: "1px solid rgba(239, 68, 68, 0.2)", marginBottom: "20px" }}>
          ⚠️ {error}
        </div>
      )}

      <OrderTable 
        orders={orders} 
        onViewPickList={handleViewPickList} 
      />

      {/* Create Order Modal */}
      {isCreateModalOpen && (
        <CreateOrderModal 
          products={products}
          onClose={() => setIsCreateModalOpen(false)}
          onSubmit={handleCreateOrderSubmit}
        />
      )}

      {/* Pick List & Dispatch Modal */}
      {activePickList && (
        <PickListModal 
          pickListData={activePickList}
          onClose={() => setActivePickList(null)}
          onConfirmDispatch={handleConfirmDispatch}
        />
      )}
    </div>
  );
}

export default OrderPage;