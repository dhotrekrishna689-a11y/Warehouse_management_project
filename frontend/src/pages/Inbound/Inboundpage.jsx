import { useEffect, useMemo, useState } from "react";
import { getProducts } from "../../services/productsApi";
import { getInboundRacks, receiveShipment } from "../../services/inboundApi";

const newItem = () => ({ product_id: "", batch_number: "", expected_quantity: "", quantity: "", rack_id: "", manufacturing_date: "", expiry_date: "", verified: false });

function InboundPage() {
  const [step, setStep] = useState(1);
  const [products, setProducts] = useState([]);
  const [racks, setRacks] = useState([]);
  const [receivedDate, setReceivedDate] = useState(new Date().toISOString().slice(0, 10));
  const [items, setItems] = useState([newItem()]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    Promise.all([getProducts(), getInboundRacks()])
      .then(([productData, rackData]) => { setProducts(productData); setRacks(rackData); })
      .catch((err) => setError(err.message || "Could not load inbound form data."));
  }, []);

  const totals = useMemo(() => items.reduce((summary, item) => ({
    expected: summary.expected + Number(item.expected_quantity || 0),
    received: summary.received + Number(item.quantity || 0),
  }), { expected: 0, received: 0 }), [items]);

  const changeItem = (index, field, value) => setItems((current) => current.map((item, itemIndex) => itemIndex === index ? { ...item, [field]: value } : item));
  const removeItem = (index) => setItems((current) => current.length === 1 ? current : current.filter((_, itemIndex) => itemIndex !== index));
  const advance = () => {
    setError("");
    if (step === 1 && items.some((item) => !item.product_id || !item.batch_number || !item.expected_quantity)) return setError("Add product, batch number, and expected quantity for every item.");
    if (step === 2 && items.some((item) => !item.quantity || !item.verified)) return setError("Enter received quantity and verify every item before continuing.");
    if (step === 3 && items.some((item) => !item.rack_id || !item.manufacturing_date || !item.expiry_date)) return setError("Assign a rack and dates for every item.");
    setStep((current) => Math.min(3, current + 1));
  };
  const submit = async () => {
    setError("");
    if (items.some((item) => !item.rack_id || !item.manufacturing_date || !item.expiry_date)) return setError("Complete rack and date assignment for all items.");
    setSubmitting(true);
    try {
      const payload = await receiveShipment({ received_date: receivedDate, items: items.map(({ expected_quantity, verified, ...item }) => ({ ...item, product_id: Number(item.product_id), rack_id: Number(item.rack_id), quantity: Number(item.quantity) })) });
      setSuccess(`${payload.message} ${payload.shipment?.shipment_number || ""}`.trim());
      setItems([newItem()]);
      setStep(1);
    } catch (err) { setError(err.message || "Could not receive shipment."); }
    finally { setSubmitting(false); }
  };

  return <section className="inbound-page">
    <div className="storage-page__header"><div><p className="eyebrow">Inbound operations</p><h1>Receive Shipment</h1><p className="page-subtitle">Record incoming stock, verify quantities, and place each item in a rack.</p></div><div className="inbound-date"><label>Received date<input type="date" value={receivedDate} onChange={(event) => setReceivedDate(event.target.value)} /></label></div></div>
    <div className="inbound-steps">{["Receive Shipment", "Verify Quantity", "Assign Rack"].map((label, index) => <button key={label} className={step === index + 1 ? "active" : step > index + 1 ? "complete" : ""} onClick={() => index + 1 < step && setStep(index + 1)}><span>{step > index + 1 ? "✓" : index + 1}</span>{label}</button>)}</div>
    {error && <div className="storage-alert">{error}</div>}{success && <div className="inbound-success">{success}</div>}
    <div className="inbound-summary"><Metric label="Line items" value={items.length} /><Metric label="Expected units" value={totals.expected} /><Metric label="Received units" value={totals.received} /></div>
    {step === 1 && <div className="storage-card inbound-card"><div className="inbound-card__heading"><div><h2>Shipment items</h2><p>Add every product included in this delivery.</p></div><button className="secondary-button" onClick={() => setItems((current) => [...current, newItem()])}>+ Add item</button></div><div className="inbound-items">{items.map((item, index) => <article className="inbound-item" key={index}><div className="item-number">{index + 1}</div><div className="inbound-fields"><Select label="Product" value={item.product_id} onChange={(value) => changeItem(index, "product_id", value)} options={products.map((product) => ({ value: product.product_id, label: product.name }))} /><Input label="Batch number" value={item.batch_number} onChange={(value) => changeItem(index, "batch_number", value)} placeholder="e.g. BATCH-2026-001" /><Input label="Expected quantity" type="number" value={item.expected_quantity} onChange={(value) => changeItem(index, "expected_quantity", value)} /></div>{items.length > 1 && <button className="danger-text remove-item" onClick={() => removeItem(index)}>Remove</button>}</article>)}</div><div className="inbound-actions"><button className="primary-button" onClick={advance}>Continue to quantity check</button></div></div>}
    {step === 2 && <div className="storage-card inbound-card"><div className="inbound-card__heading"><div><h2>Verify received quantity</h2><p>Match physical stock with the delivery note before storage.</p></div></div><div className="verify-list">{items.map((item, index) => <article className="verify-row" key={index}><strong>{products.find((product) => String(product.product_id) === String(item.product_id))?.name || "Product"}</strong><span>Batch {item.batch_number}</span><span>Expected: {item.expected_quantity}</span><label>Received<input type="number" min="1" value={item.quantity} onChange={(event) => changeItem(index, "quantity", event.target.value)} /></label><label className="verify-check"><input type="checkbox" checked={item.verified} onChange={(event) => changeItem(index, "verified", event.target.checked)} /> Verified</label></article>)}</div><div className="inbound-actions"><button className="secondary-button" onClick={() => setStep(1)}>Back</button><button className="primary-button" onClick={advance}>Continue to rack assignment</button></div></div>}
    {step === 3 && <div className="storage-card inbound-card"><div className="inbound-card__heading"><div><h2>Assign storage rack</h2><p>Choose where each verified item should be stored.</p></div></div><div className="assign-list">{items.map((item, index) => <article className="assign-row" key={index}><strong>{products.find((product) => String(product.product_id) === String(item.product_id))?.name || "Product"}</strong><span>{item.quantity} units · {item.batch_number}</span><Select label="Destination rack" value={item.rack_id} onChange={(value) => changeItem(index, "rack_id", value)} options={racks.map((rack) => ({ value: rack.rack_id, label: `${rack.rack_code} — capacity ${rack.capacity}` }))} /><Input label="Manufacturing date" type="date" value={item.manufacturing_date} onChange={(value) => changeItem(index, "manufacturing_date", value)} /><Input label="Expiry date" type="date" value={item.expiry_date} onChange={(value) => changeItem(index, "expiry_date", value)} /></article>)}</div><div className="inbound-actions"><button className="secondary-button" onClick={() => setStep(2)}>Back</button><button className="primary-button" disabled={submitting} onClick={submit}>{submitting ? "Receiving…" : "Receive shipment"}</button></div></div>}
  </section>;
}

function Metric({ label, value }) { return <article className="metric-card"><span>{label}</span><strong>{value}</strong></article>; }
function Input({ label, value, onChange, type = "text", placeholder = "" }) { return <label className="inbound-input">{label}<input type={type} min={type === "number" ? "1" : undefined} value={value} onChange={(event) => onChange(event.target.value)} placeholder={placeholder} required /></label>; }
function Select({ label, value, onChange, options }) { return <label className="inbound-input">{label}<select value={value} onChange={(event) => onChange(event.target.value)} required><option value="">Select {label.toLowerCase()}</option>{options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>; }

export default InboundPage;
