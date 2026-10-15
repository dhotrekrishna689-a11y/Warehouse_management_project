import { useState } from "react";
import { confirmSupplierOrder, getPendingSupplierOrders, getSupplierOrder, prepareSupplierOrder } from "../../services/supplierOrdersApi";

const today = new Date().toISOString().slice(0, 10);

function SupplierOrdersPage() {
  const [supplierId, setSupplierId] = useState("");
  const [orders, setOrders] = useState([]);
  const [selected, setSelected] = useState(null);
  const [dates, setDates] = useState({ expected_dispatch_date: today, expected_delivery_date: today });
  const [items, setItems] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadOrders = async (event) => {
    event.preventDefault();
    if (!supplierId) return setError("Enter a supplier ID to view its pending orders.");
    setBusy(true); setError(""); setMessage(""); setSelected(null);
    try { setOrders(await getPendingSupplierOrders(supplierId) || []); }
    catch (err) { setError(err.message); }
    finally { setBusy(false); }
  };

  const openOrder = async (orderId) => {
    setBusy(true); setError(""); setMessage("");
    try {
      const order = await getSupplierOrder(orderId);
      setSelected(order);
      setItems((order.items || []).map((item) => ({ ...item, prepared_quantity: item.ordered_quantity, manufacturing_date: today, expiry_date: "" })));
    } catch (err) { setError(err.message); }
    finally { setBusy(false); }
  };

  const updateItem = (index, field, value) => setItems((current) => current.map((item, i) => i === index ? { ...item, [field]: value } : item));

  const confirmOrder = async () => {
    if (!selected) return;
    if (!dates.expected_dispatch_date || !dates.expected_delivery_date || items.some((item) => !item.prepared_quantity || Number(item.prepared_quantity) > Number(item.ordered_quantity) || !item.manufacturing_date || !item.expiry_date)) {
      setError("Enter valid dispatch and delivery dates, quantities, manufacturing dates, and expiry dates for every item.");
      return;
    }
    setBusy(true); setError(""); setMessage("");
    try {
      await prepareSupplierOrder(selected.purchase_order_id, { ...dates, items: items.map(({ product_id, prepared_quantity, manufacturing_date, expiry_date }) => ({ product_id, prepared_quantity: Number(prepared_quantity), manufacturing_date, expiry_date: expiry_date || null })) });
      const result = await confirmSupplierOrder(selected.purchase_order_id);
      const saved = { ...result, saved_at: new Date().toISOString() };
      localStorage.setItem("warehouse-last-supplier-qr", JSON.stringify(saved));
      setMessage(`Order ${result.purchase_order_number} confirmed. Its QR code is ready in Receive Shipment.`);
      setSelected(null);
      setOrders((current) => current.filter((order) => order.purchase_order_id !== selected.purchase_order_id));
    } catch (err) { setError(err.message); }
    finally { setBusy(false); }
  };

  return <section className="supplier-page">
    <div className="storage-page__header"><div><p className="eyebrow">Supplier workspace</p><h1>Supplier Orders</h1><p className="page-subtitle">View a supplier’s pending orders, prepare items, and confirm the shipment.</p></div></div>
    <form className="storage-card supplier-filter" onSubmit={loadOrders}><label className="inbound-input">Supplier ID<input type="number" min="1" value={supplierId} onChange={(event) => setSupplierId(event.target.value)} placeholder="Enter supplier ID" /></label><button className="primary-button" disabled={busy}>{busy ? "Loading…" : "View orders"}</button></form>
    {error && <div className="storage-alert">{error}</div>}{message && <div className="inbound-success">{message}</div>}
    <div className="supplier-grid">
      <div className="storage-card"><div className="supplier-card-heading"><div><h2>Pending orders</h2><p>{orders.length} order{orders.length === 1 ? "" : "s"}</p></div></div>
        {orders.length ? <div className="supplier-order-list">{orders.map((order) => <button key={order.purchase_order_id} className={`supplier-order ${selected?.purchase_order_id === order.purchase_order_id ? "is-selected" : ""}`} onClick={() => openOrder(order.purchase_order_id)}><span><strong>{order.purchase_order_number}</strong><small>{order.items?.length || 0} products · {order.status}</small></span><span>›</span></button>)}</div> : <p className="empty-state">Enter a supplier ID to load pending purchase orders.</p>}
      </div>
      <div className="storage-card"><div className="supplier-card-heading"><div><h2>{selected ? selected.purchase_order_number : "Order details"}</h2><p>{selected ? `Supplier ${selected.supplier_id} · ${selected.status}` : "Select an order to review and prepare it."}</p></div></div>
        {selected && <div className="supplier-detail"><div className="supplier-dates"><label className="inbound-input">Dispatch date<input type="date" value={dates.expected_dispatch_date} onChange={(event) => setDates((current) => ({ ...current, expected_dispatch_date: event.target.value }))} /></label><label className="inbound-input">Delivery date<input type="date" value={dates.expected_delivery_date} onChange={(event) => setDates((current) => ({ ...current, expected_delivery_date: event.target.value }))} /></label></div>
          {items.map((item, index) => <article className="supplier-item" key={item.product_id}><div><strong>{item.product_name || `Product ${item.product_id}`}</strong><small>Ordered: {item.ordered_quantity}</small></div><label className="inbound-input">Prepared qty<input type="number" min="1" max={item.ordered_quantity} value={item.prepared_quantity} onChange={(event) => updateItem(index, "prepared_quantity", event.target.value)} /></label><label className="inbound-input">Manufactured<input type="date" value={item.manufacturing_date} onChange={(event) => updateItem(index, "manufacturing_date", event.target.value)} required /></label><label className="inbound-input">Expires<input type="date" value={item.expiry_date} onChange={(event) => updateItem(index, "expiry_date", event.target.value)} required /></label></article>)}
          <button className="primary-button" disabled={busy || !items.length} onClick={confirmOrder}>{busy ? "Processing…" : "Prepare, confirm & generate QR"}</button>
        </div>}
      </div>
    </div>
  </section>;
}

export default SupplierOrdersPage;
