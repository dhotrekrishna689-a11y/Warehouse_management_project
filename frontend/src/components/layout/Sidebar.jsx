/*
function Sidebar() {
  return (
    <aside>
      <h2>Smart Warehouse</h2>

      <nav>
        <div>Dashboard</div>
        <div>Inventory</div>
        <div>Inbound</div>
        <div>Orders</div>
        <div>Racks</div>
      </nav>
    </aside>
  );
}

export default Sidebar;*/

//import { Link } from "react-router-dom";
import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>Smart Warehouse</h2>

      <nav>
        <NavLink 
            to="/"
            className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
            }
        >Dashboard</NavLink>


        <NavLink 
            to="/inventory"
            className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
            }
        >Inventory</NavLink>

        <NavLink 
            to="/inbound"
            className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
            }
        >Inbound</NavLink>

        <NavLink 
            to="/order"
            end
            className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
            }
        
        
        >Orders</NavLink>

        <NavLink 
            to="/rack"
            className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
            }
        
        >Racks</NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;