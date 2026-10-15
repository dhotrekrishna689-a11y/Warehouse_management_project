import { useEffect, useState } from "react";
import { getProducts } from "../../services/productsApi";
import { placePurchaseOrder } from "../../services/purchaseOrdersApi";

function PlaceSupplierOrderPage() {
  const [products, setProducts] = useState([]);
  const [supplierId, setSupplierId] = useState("");
  const [items, setItems] = useState([{ product_id: "", quantity: "" }]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => { getProducts().then(setProducts).catch((err) => setError(err.message || "Could not load products.")); }, []);
  const updateItem = (index, field, value) => setItems((current) => current.map((item, i) => i === index ? { ...item, [field]: value } : item));
  const submit = async (event) => {
    event.preventDefault(); setError(""); setSuccess("");
    if (!supplierId || items.some((item) => !item.product_id || Number(item.quantity) <= 0)) return setError("Choose a supplier, product, and quantity for every order line.");
    setBusy(true);
    try {
      const result = await placePurchaseOrder(supplierId, items);
      const orderNumber = result.data?.purchase_order_number;
      setSuccess(`${result.message || "Purchase order sent to supplier."}${orderNumber ? ` ${orderNumber}.` : ""} The supplier can now see it in Supplier Orders.`);
      setItems([{ product_id: "", quantity: "" }]);
    } catch (err) { setError(err.message || "Could not place the supplier order."); }
    finally { setBusy(false); }
  };

  return <section className="supplier-page">
    <div className="storage-page__header"><div><p className="eyebrow">Warehouse purchasing</p><h1>Place Supplier Order</h1><p className="page-subtitle">Send a purchase order directly to a supplier. It will appear in that supplier’s pending orders.</p></div></div>
    {error && <div className="storage-alert">{error}</div>}{success && <div className="inbound-success">{success}</div>}
    <form className="storage-card place-order-form" onSubmit={submit}>
      <label className="inbound-input supplier-id-input">Supplier ID<input type="number" min="1" value={supplierId} onChange={(event) => setSupplierId(event.target.value)} placeholder="Enter supplier ID" required /></label>
      <div className="supplier-card-heading"><div><h2>Order items</h2><p>Select products and quantities to send.</p></div><button className="secondary-button" type="button" onClick={() => setItems((current) => [...current, { product_id: "", quantity: "" }])}>+ Add item</button></div>
      <div className="place-order-items">{items.map((item, index) => <div className="place-order-row" key={index}><label className="inbound-input">Product<select value={item.product_id} onChange={(event) => updateItem(index, "product_id", event.target.value)} required><option value="">Choose product</option>{products.map((product) => <option key={product.product_id} value={product.product_id}>{product.name} · {product.sku}</option>)}</select></label><label className="inbound-input">Quantity<input type="number" min="1" value={item.quantity} onChange={(event) => updateItem(index, "quantity", event.target.value)} required /></label>{items.length > 1 && <button className="danger-text" type="button" onClick={() => setItems((current) => current.filter((_, i) => i !== index))}>Remove</button>}</div>)}</div>
      <div className="inbound-actions"><span className="scanner-note">The supplier will see this order under the entered supplier ID.</span><button className="primary-button" disabled={busy}>{busy ? "Sending order…" : "Send order to supplier"}</button></div>
    </form>
  </section>;
}

export default PlaceSupplierOrderPage;
