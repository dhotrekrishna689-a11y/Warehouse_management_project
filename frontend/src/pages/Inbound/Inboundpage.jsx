import { useEffect, useRef, useState } from "react";
import { getRackUtilization } from "../../services/rackApi";
import { receiveShipment } from "../../services/inboundApi";

function localDate() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
}

function InboundPage() {
  const videoRef = useRef(null);
  const scannerControlsRef = useRef(null);
  const [scanning, setScanning] = useState(false);
  const [shipment, setShipment] = useState(null);
  const [supplierQrImage, setSupplierQrImage] = useState("");
  const [rackOptions, setRackOptions] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    getRackUtilization().then(setRackOptions).catch((err) => setError(err.message || "Could not load warehouse racks."));
  }, []);

  useEffect(() => {
    try {
      const savedQr = JSON.parse(localStorage.getItem("warehouse-last-supplier-qr") || "null");
      if (savedQr?.qr_code) {
        const parsed = parseSupplierQr(JSON.stringify(savedQr));
        setSupplierQrImage(savedQr.qr_code);
        setShipment({ ...parsed, items: parsed.items.map((item) => ({ ...item, received_quantity: "", rack_id: "" })) });
      }
    } catch { setSupplierQrImage(""); }
  }, []);

  const stopCamera = () => {
    scannerControlsRef.current?.stop();
    scannerControlsRef.current = null;
    setScanning(false);
  };

  useEffect(() => {
    if (!scanning || !videoRef.current) return undefined;
    let active = true;
    let controls;
    import("@zxing/browser").then(({ BrowserQRCodeReader }) => {
      if (!active) return null;
      const reader = new BrowserQRCodeReader();
      return reader.decodeFromConstraints({ audio: false, video: { facingMode: { ideal: "environment" } } }, videoRef.current, (result, _decodeError, currentControls) => {
        if (!active) return;
        controls = currentControls;
        scannerControlsRef.current = currentControls;
        if (!result) return;
        try {
          const parsed = parseSupplierQr(result.getText());
          setShipment({ ...parsed, items: parsed.items.map((item) => ({ ...item, received_quantity: "", rack_id: "" })) });
          setSupplierQrImage(getSavedQrImage(parsed.purchase_order_id));
          currentControls.stop();
          scannerControlsRef.current = null;
          setScanning(false);
        } catch (err) {
          setError(err.message || "Could not read this supplier QR code.");
          currentControls.stop();
          scannerControlsRef.current = null;
          setScanning(false);
        }
      });
    }).then((createdControls) => {
      controls = createdControls || controls;
      if (!active) controls?.stop();
    }).catch((err) => {
      if (!active) return;
      setError(err.name === "NotAllowedError" ? "Allow camera access to scan the supplier QR code." : err.message || "Could not open the camera.");
      setScanning(false);
    });
    return () => {
      active = false;
      controls?.stop();
      scannerControlsRef.current?.stop();
      scannerControlsRef.current = null;
    };
  }, [scanning]);

  const startScanner = async () => {
    setError(""); setSuccess(""); setShipment(null);
    setSupplierQrImage("");
    if (!navigator.mediaDevices?.getUserMedia) {
      setError("Camera access is unavailable. Open the app on localhost or over HTTPS.");
      return;
    }
    setScanning(true);
  };

  const updateReceivedQuantity = (index, value) => setShipment((current) => ({
    ...current,
    items: current.items.map((item, itemIndex) => itemIndex === index ? { ...item, received_quantity: value } : item),
  }));

  const updateRack = (index, value) => setShipment((current) => ({
    ...current,
    items: current.items.map((item, itemIndex) => itemIndex === index ? { ...item, rack_id: value } : item),
  }));

  const receiveScannedShipment = async () => {
    if (!shipment) return;
    if (shipment.items.some((item) => item.received_quantity === "" || Number(item.received_quantity) < 0)) {
      setError("Count and enter the received quantity for each product.");
      return;
    }
    const countedItems = shipment.items.filter((item) => Number(item.received_quantity) > 0);
    if (!countedItems.length) {
      setError("Enter at least one received unit to continue.");
      return;
    }
    setSubmitting(true); setError(""); setSuccess("");
    try {
      if (!rackOptions.length) throw new Error("No warehouse racks are available. Add a rack before receiving this shipment.");
      const rackLoads = new Map();
      const items = countedItems.map((item) => {
        const quantity = Number(item.received_quantity);
        if (!Number.isInteger(quantity)) throw new Error(`Enter a whole unit count for product ${item.product_id}.`);
        const rack = rackOptions.find((candidate) => String(candidate.rack_id) === String(item.rack_id));
        if (!rack) throw new Error(`Choose a rack for product ${item.product_id}.`);
        const alreadyAssigned = rackLoads.get(rack.rack_id) || 0;
        const freeCapacity = Number(rack.capacity || 0) - Number(rack.current_stock || 0);
        if (alreadyAssigned + quantity > freeCapacity) throw new Error(`${rack.rack_code} does not have enough free capacity for the selected items.`);
        rackLoads.set(rack.rack_id, alreadyAssigned + quantity);
        return { product_id: Number(item.product_id), batch_number: item.batch_number, quantity, manufacturing_date: item.manufacturing_date, expiry_date: item.expiry_date, rack_id: Number(item.rack_id) };
      });
      const result = await receiveShipment({ purchase_order_id: Number(shipment.purchase_order_id), received_date: localDate(), items });
      setSuccess(`${shipment.shipment_number} received successfully. ${result.shipment?.shipment_number || ""}`.trim());
      try {
        const latest = JSON.parse(localStorage.getItem("warehouse-last-supplier-qr") || "null");
        if (latest?.purchase_order_id === shipment.purchase_order_id) localStorage.removeItem("warehouse-last-supplier-qr");
      } catch { localStorage.removeItem("warehouse-last-supplier-qr"); }
      setShipment(null);
      setSupplierQrImage("");
    } catch (err) { setError(err.message || "Could not receive the scanned shipment."); }
    finally { setSubmitting(false); }
  };

  return <section className="inbound-page">
    <div className="storage-page__header"><div><p className="eyebrow">Warehouse receiving</p><h1>Receive Shipment</h1><p className="page-subtitle">Scan the QR code supplied with the delivery. Shipment and batch details will be read automatically.</p></div></div>
    {error && <div className="storage-alert">{error}</div>}{success && <div className="inbound-success">{success}</div>}
    <div className="storage-card scanner-card">
      {!scanning && !shipment && <div className="scanner-start"><div className="scanner-icon" aria-hidden="true">▦</div><h2>Scan supplier QR</h2><p>Point the camera at the supplier’s QR code.</p><button className="primary-button" onClick={startScanner}>Open QR scanner</button></div>}
      {scanning && <div className="scanner-live"><div className="scanner-video-wrap"><video ref={videoRef} muted playsInline /><div className="scanner-target" /></div><p>Hold the supplier QR code inside the frame.</p><button className="secondary-button" onClick={stopCamera}>Stop scanner</button></div>}
      {shipment && <div className="scanned-shipment"><div className="scanned-heading"><div><p className="eyebrow">Supplier QR</p><h2>{shipment.shipment_number}</h2><p className="page-subtitle">Purchase order {shipment.purchase_order_number} · {shipment.items.length} products</p></div>{supplierQrImage && <img className="inbound-qr-image" src={supplierQrImage} alt={`Supplier QR for ${shipment.shipment_number}`} />}</div><div className="scanned-items">{shipment.items.map((item, index) => <div className="scanned-item" key={`${item.product_id}-${item.batch_number}`}><span><strong>Product {item.product_id}</strong><small>Supplier quantity: {item.prepared_quantity} · Batch {item.batch_number}</small></span><label className="inbound-input">Received quantity<input type="number" min="0" step="1" value={item.received_quantity} onChange={(event) => updateReceivedQuantity(index, event.target.value)} placeholder="Count received" /></label><label className="inbound-input">Rack<select value={item.rack_id} onChange={(event) => updateRack(index, event.target.value)}><option value="">Choose rack</option>{rackOptions.map((rack) => { const free = Number(rack.capacity || 0) - Number(rack.current_stock || 0); return <option key={rack.rack_id} value={rack.rack_id}>{rack.rack_code} · {free} free</option>; })}</select></label></div>)}</div><div className="inbound-actions"><button className="secondary-button" onClick={() => { setShipment(null); setSupplierQrImage(""); }}>Scan another QR</button><button className="primary-button" disabled={submitting} onClick={receiveScannedShipment}>{submitting ? "Receiving…" : "Receive shipment"}</button></div></div>}
    </div>
  </section>;
}

function parseSupplierQr(rawValue) {
  let parsed;
  try { parsed = JSON.parse(rawValue); }
  catch { throw new Error("This QR code does not contain supplier shipment data."); }
  if (!parsed.shipment_number || !parsed.purchase_order_id || !Array.isArray(parsed.items) || !parsed.items.length) throw new Error("This QR code does not contain a supplier shipment.");
  const missing = parsed.items.some((item) => !item.product_id || !item.batch_number || !item.prepared_quantity || !item.manufacturing_date || !item.expiry_date);
  if (missing) throw new Error("The supplier QR is missing required batch or expiry details.");
  return parsed;
}

function getSavedQrImage(purchaseOrderId) {
  try {
    const latest = JSON.parse(localStorage.getItem("warehouse-last-supplier-qr") || "null");
    return String(latest?.purchase_order_id) === String(purchaseOrderId) ? latest.qr_code || "" : "";
  } catch { return ""; }
}

export default InboundPage;
