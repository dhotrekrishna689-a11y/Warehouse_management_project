import { Routes, Route } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
import DashboardPage from "../pages/Dashboard/DashboardPage";
import InventoryPage from "../pages/Inventory/InventoryPage";
import OrderPage from "../pages/Order/OrderPage";
import InboundPage from "../pages/Inbound/Inboundpage";
import RackPage from "../pages/Rack/Rackpage";
import SupplierOrdersPage from "../pages/SupplierOrders/SupplierOrdersPage";
import PlaceSupplierOrderPage from "../pages/PlaceSupplierOrder/PlaceSupplierOrderPage";

function AppRoutes() {
  return (
    <Routes>
      <Route  element={<MainLayout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/inventory" element={<InventoryPage />} />
        <Route path="/order" element={<OrderPage />} />
        <Route path="/warehouse" element={<InboundPage />} />
        <Route path="/inbound" element={<InboundPage />} />
        <Route path="/rack" element={<RackPage />} />
        <Route path="/supplier-orders" element={<SupplierOrdersPage />} />
        <Route path="/place-supplier-order" element={<PlaceSupplierOrderPage />} />
      </Route>  
    </Routes>
  );
}

export default AppRoutes;
