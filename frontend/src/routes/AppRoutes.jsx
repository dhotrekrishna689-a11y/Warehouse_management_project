import { Routes, Route } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
import DashboardPage from "../pages/Dashboard/DashboardPage";
import InventoryPage from "../pages/Inventory/InventoryPage";
import OrderPage from "../pages/Order/OrderPage";
import InboundPage from "../pages/Inbound/InboundPage";
import RackPage from "../pages/Rack/RackPage";

function AppRoutes() {
  return (
    <Routes>
      <Route  element={<MainLayout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/inventory" element={<InventoryPage />} />
        <Route path="/order" element={<OrderPage />} />
        <Route path="/inbound" element={<InboundPage />} />
        <Route path="/rack" element={<RackPage />} />
      </Route>  
    </Routes>
  );
}

export default AppRoutes;