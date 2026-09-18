import { useEffect, useMemo, useState } from "react";
import { getInventories } from "../../services/inventoryApi";
import { getProducts } from "../../services/productsApi";
import {
  createRack,
  deleteRack,
  getBatches,
  getRackUtilization,
  getRacks,
  moveProduct,
  updateRack,
} from "../../services/rackApi";

const EMPTY_MOVEMENT = {
  product_id: "",
  batch_id: "",
  source_rack_id: "",
  destination_rack_id: "",
  quantity: "",
  reason: "",
};

function RackPage() {
  const [tab, setTab] = useState("racks");
  const [racks, setRacks] = useState([]);
  const [utilization, setUtilization] = useState([]);
  const [inventories, setInventories] = useState([]);
  const [products, setProducts] = useState([]);
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [rackCode, setRackCode] = useState("");
  const [rackCapacity, setRackCapacity] = useState("");
  const [editingRack, setEditingRack] = useState(null);
  const [movement, setMovement] = useState(EMPTY_MOVEMENT);
  const [submitting, setSubmitting] = useState(false);

  const loadData = async () => {
    setLoading(true);
    setError("");
    try {
      const [rackData, utilizationData, inventoryData, productData, batchData] = await Promise.all([
        getRacks(),
        getRackUtilization(),
        getInventories(),
        getProducts(),
        getBatches(),
      ]);
      setRacks(rackData.filter(Boolean));
      setUtilization(utilizationData);
      setInventories(inventoryData);
      setProducts(productData);
      setBatches(batchData);
    } catch (requestError) {
      setError(requestError.message || "Could not load storage data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const rackDetails = useMemo(() => {
    const usageById = new Map(utilization.map((item) => [item.rack_id, item]));
    return racks.map((rack) => {
      const usage = usageById.get(rack.rack_id) || {};
      const capacity = Number(usage.capacity ?? rack.capacity ?? 0);
      const stock = Number(usage.current_stock ?? 0);
      const percent = capacity ? Math.min(100, Math.round((stock / capacity) * 100)) : 0;
      return { ...rack, capacity, stock, percent };
    });
  }, [racks, utilization]);

  const filteredRacks = rackDetails.filter((rack) =>
    (rack.rack_code || "").toLowerCase().includes(search.toLowerCase()),
  );
  const totalCapacity = rackDetails.reduce((total, rack) => total + rack.capacity, 0);
  const usedCapacity = rackDetails.reduce((total, rack) => total + rack.stock, 0);
  const selectedBatches = batches.filter(
    (batch) => String(batch.product_id) === String(movement.product_id),
  );
  const selectedProduct = products.find(
    (product) => String(product.product_id) === String(movement.product_id),
  );
  const selectedBatch = batches.find(
    (batch) => String(batch.batch_id) === String(movement.batch_id),
  );
  const sourceRackOptions = inventories
    .filter((inventory) =>
      inventory.quantity > 0 &&
      inventory.product_name === selectedProduct?.name &&
      inventory.batch_name === selectedBatch?.batch_number,
    )
    .map((inventory) => {
      const rack = rackDetails.find((item) => item.rack_code === inventory.rack_number);
      return rack && {
        value: rack.rack_id,
        label: `${rack.rack_code} (${inventory.quantity} available)`,
      };
    })
    .filter(Boolean);
  const destinationRackOptions = rackDetails
    .filter((rack) => String(rack.rack_id) !== String(movement.source_rack_id))
    .map((rack) => ({
      value: rack.rack_id,
      label: `${rack.rack_code} (${rack.percent}% used)`,
    }));

  const saveRack = async (event) => {
    event.preventDefault();
    if (!rackCode.trim()) return;
    setSubmitting(true);
    setError("");
    try {
      if (editingRack) {
        await updateRack(editingRack.rack_id, rackCode.trim());
      } else {
        await createRack(rackCode.trim(), rackCapacity);
      }
      setRackCode("");
      setRackCapacity("");
      setEditingRack(null);
      await loadData();
    } catch (requestError) {
      setError(requestError.message || "Could not save the rack.");
    } finally {
      setSubmitting(false);
    }
  };

  const removeRack = async (rack) => {
    if (!window.confirm(`Delete rack ${rack.rack_code}?`)) return;
    try {
      await deleteRack(rack.rack_id);
      await loadData();
    } catch (requestError) {
      setError(requestError.message || "Could not delete the rack.");
    }
  };

  const submitMovement = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await moveProduct({
        ...movement,
        product_id: Number(movement.product_id),
        batch_id: Number(movement.batch_id),
        source_rack_id: Number(movement.source_rack_id),
        destination_rack_id: Number(movement.destination_rack_id),
        quantity: Number(movement.quantity),
      });
      setMovement(EMPTY_MOVEMENT);
      await loadData();
    } catch (requestError) {
      setError(requestError.message || "Could not move the product.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="storage-page">
      <div className="storage-page__header">
        <div>
          <p className="eyebrow">Warehouse operations</p>
          <h1>Rack &amp; Storage</h1>
          <p className="page-subtitle">Manage rack locations, move stock, and monitor space usage.</p>
        </div>
        <button className="secondary-button" onClick={loadData} disabled={loading}>Refresh data</button>
      </div>

      <div className="storage-tabs" role="tablist" aria-label="Rack and storage sections">
        <button className={tab === "racks" ? "active" : ""} onClick={() => setTab("racks")}>Rack Management</button>
        <button className={tab === "movement" ? "active" : ""} onClick={() => setTab("movement")}>Product Movement</button>
        <button className={tab === "heatmap" ? "active" : ""} onClick={() => setTab("heatmap")}>Warehouse Heatmap</button>
      </div>

      {error && <div className="storage-alert">{error}</div>}

      {tab === "racks" && (
        <>
          <div className="storage-metrics">
            <Metric label="Total racks" value={rackDetails.length} />
            <Metric label="Total capacity" value={totalCapacity.toLocaleString()} />
            <Metric label="Stock stored" value={usedCapacity.toLocaleString()} />
            <Metric label="Utilization" value={`${totalCapacity ? Math.round((usedCapacity / totalCapacity) * 100) : 0}%`} />
          </div>
          <div className="storage-split">
            <form className="storage-card rack-form" onSubmit={saveRack}>
              <h2>{editingRack ? "Edit rack" : "Add new rack"}</h2>
              <label htmlFor="rack-code">Rack code</label>
              <input id="rack-code" value={rackCode} onChange={(event) => setRackCode(event.target.value)} placeholder="e.g. A-01-03" required />
              <label htmlFor="rack-capacity">Storage capacity</label>
              <input id="rack-capacity" type="number" min="1" value={rackCapacity} onChange={(event) => setRackCapacity(event.target.value)} placeholder="e.g. 500" required={!editingRack} disabled={Boolean(editingRack)} />
              <div className="form-actions">
                {editingRack && <button type="button" className="text-button" onClick={() => { setEditingRack(null); setRackCode(""); setRackCapacity(""); }}>Cancel</button>}
                <button className="primary-button" disabled={submitting}>{editingRack ? "Save changes" : "Create rack"}</button>
              </div>
            </form>
            <div className="storage-card storage-tip"><span>◈</span><div><h2>Storage rule</h2><p>Racks with inventory cannot be deleted. Move stock first, then remove the empty rack.</p></div></div>
          </div>
          <div className="storage-toolbar"><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search rack code" /><span>{filteredRacks.length} rack{filteredRacks.length === 1 ? "" : "s"}</span></div>
          <div className="storage-card rack-table-wrap">
            <table className="rack-table"><thead><tr><th>Rack</th><th>Stock / capacity</th><th>Utilization</th><th>Status</th><th aria-label="Actions" /></tr></thead>
              <tbody>{filteredRacks.map((rack) => <tr key={rack.rack_id}><td><strong>{rack.rack_code}</strong></td><td>{rack.stock.toLocaleString()} / {rack.capacity.toLocaleString()}</td><td><div className="usage"><span><i style={{ width: `${rack.percent}%` }} /></span>{rack.percent}%</div></td><td><Status percent={rack.percent} /></td><td className="row-actions"><button onClick={() => { setEditingRack(rack); setRackCode(rack.rack_code); setRackCapacity(rack.capacity); }}>Edit</button><button className="danger-text" onClick={() => removeRack(rack)}>Delete</button></td></tr>)}</tbody>
            </table>
            {!loading && !filteredRacks.length && <p className="empty-state">No racks found. Add your first rack above.</p>}
          </div>
        </>
      )}

      {tab === "movement" && <form className="storage-card movement-form" onSubmit={submitMovement}>
        <div><h2>Move product between racks</h2><p>Select a product, its batch, source rack and destination rack.</p></div>
        <div className="form-grid">
          <Select label="Product" value={movement.product_id} onChange={(value) => setMovement({ ...movement, product_id: value, batch_id: "", source_rack_id: "" })} options={products.map((product) => ({ value: product.product_id, label: product.name }))} />
          <Select label="Batch" value={movement.batch_id} onChange={(value) => setMovement({ ...movement, batch_id: value, source_rack_id: "" })} options={selectedBatches.map((batch) => ({ value: batch.batch_id, label: batch.batch_number }))} disabled={!movement.product_id} />
          <Select label="Source rack" value={movement.source_rack_id} onChange={(value) => {
            const firstDestination = rackDetails.find((rack) => String(rack.rack_id) !== String(value));
            setMovement({ ...movement, source_rack_id: value, destination_rack_id: firstDestination ? String(firstDestination.rack_id) : "" });
          }} options={sourceRackOptions} disabled={!movement.batch_id} />
          <div className="select-with-hint">
            <Select label="Destination rack" value={movement.destination_rack_id} onChange={(value) => setMovement({ ...movement, destination_rack_id: value })} options={destinationRackOptions} disabled={!movement.source_rack_id || !destinationRackOptions.length} />
            {movement.source_rack_id && !destinationRackOptions.length && <small>Add another rack before moving stock.</small>}
          </div>
          <label>Quantity<input type="number" min="1" value={movement.quantity} onChange={(event) => setMovement({ ...movement, quantity: event.target.value })} required /></label>
          <label>Reason<input value={movement.reason} onChange={(event) => setMovement({ ...movement, reason: event.target.value })} placeholder="e.g. Optimise picking path" required /></label>
        </div>
        <button className="primary-button" disabled={submitting}>Move product</button>
      </form>}

      {tab === "heatmap" && <div className="storage-card heatmap"><div><h2>Warehouse heatmap</h2><p>Colour shows how full each rack is based on its current stock and capacity.</p></div><div className="heatmap-legend"><span className="low">0–49%</span><span className="medium">50–79%</span><span className="high">80–100%</span></div><div className="heatmap-grid">{rackDetails.map((rack) => <article className={`heatmap-cell ${rack.percent >= 80 ? "is-high" : rack.percent >= 50 ? "is-medium" : "is-low"}`} key={rack.rack_id}><strong>{rack.rack_code}</strong><span>{rack.percent}% full</span><small>{rack.stock} / {rack.capacity}</small></article>)}</div>{!loading && !rackDetails.length && <p className="empty-state">Add racks to see the warehouse heatmap.</p>}</div>}
    </section>
  );
}

function Metric({ label, value }) { return <article className="metric-card"><span>{label}</span><strong>{value}</strong></article>; }
function Status({ percent }) { const label = percent >= 80 ? "Near full" : percent >= 50 ? "In use" : "Available"; return <span className={`status status--${percent >= 80 ? "high" : percent >= 50 ? "medium" : "low"}`}>{label}</span>; }
function Select({ label, value, onChange, options, disabled = false }) { return <label>{label}<select value={value} onChange={(event) => onChange(event.target.value)} disabled={disabled} required><option value="">Select {label.toLowerCase()}</option>{options.map((option) => <option value={option.value} key={option.value}>{option.label}</option>)}</select></label>; }

export default RackPage;
