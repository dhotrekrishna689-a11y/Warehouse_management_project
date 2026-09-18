import { useEffect, useState } from "react";
import { getDashboard } from "../../services/dashboardApi";

/* ─── tiny helpers ─────────────────────────────────────────────────────────── */

function KpiCard({ label, value, sub, accent }) {
  return (
    <article className="dash-kpi" style={{ "--accent": accent }}>
      <span className="dash-kpi__label">{label}</span>
      <strong className="dash-kpi__value">{value}</strong>
      {sub && <span className="dash-kpi__sub">{sub}</span>}
    </article>
  );
}

function SectionHead({ title, count }) {
  return (
    <div className="dash-section-head">
      <h2>{title}</h2>
      {count !== undefined && <span className="dash-badge">{count}</span>}
    </div>
  );
}

function MovementTag({ type }) {
  const map = {
    RECEIVED:   { color: "#10b981", bg: "rgba(16,185,129,.12)"  },
    PICKED:     { color: "#8b5cf6", bg: "rgba(139,92,246,.12)"  },
    ADJUSTMENT: { color: "#f59e0b", bg: "rgba(245,158,11,.12)"  },
    MOVED_OUT:  { color: "#64748b", bg: "rgba(100,116,139,.12)" },
    MOVED_IN:   { color: "#3b82f6", bg: "rgba(59,130,246,.12)"  },
    DISPATCHED: { color: "#ef4444", bg: "rgba(239,68,68,.12)"   },
  };
  const s = map[type] || { color: "#94a3b8", bg: "rgba(148,163,184,.12)" };
  return (
    <span
      style={{
        color: s.color,
        background: s.bg,
        padding: "2px 9px",
        borderRadius: "20px",
        fontSize: "11px",
        fontWeight: 700,
        letterSpacing: ".4px",
        whiteSpace: "nowrap",
      }}
    >
      {type}
    </span>
  );
}

function UtilBar({ percent }) {
  const color =
    percent >= 80 ? "#ef4444" : percent >= 50 ? "#f59e0b" : "#10b981";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div
        style={{
          flex: 1,
          height: 6,
          borderRadius: 4,
          background: "rgba(255,255,255,.07)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${percent}%`,
            height: "100%",
            background: color,
            borderRadius: 4,
            transition: "width .5s ease",
          }}
        />
      </div>
      <span style={{ fontSize: 12, color, fontWeight: 600, minWidth: 34 }}>
        {percent}%
      </span>
    </div>
  );
}

/* ─── main component ───────────────────────────────────────────────────────── */

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getDashboard()
      .then(setData)
      .catch((e) => setError(e.message || "Could not load dashboard."))
      .finally(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="dash-loading">
        <span className="dash-spinner" />
        Loading dashboard…
      </div>
    );

  if (error)
    return <div className="dash-error">⚠ {error}</div>;

  const { kpis, low_stock, pending_orders, rack_utilization, aging_stock, recent_movements } = data;

  return (
    <div className="dash">
      {/* ── header ── */}
      <div className="dash-header">
        <div>
          <p className="eyebrow">Warehouse overview</p>
          <h1>Dashboard</h1>
        </div>
        <button
          className="secondary-button"
          onClick={() => {
            setLoading(true);
            getDashboard()
              .then(setData)
              .catch((e) => setError(e.message))
              .finally(() => setLoading(false));
          }}
        >
          Refresh
        </button>
      </div>

      {/* ── KPI row ── */}
      <div className="dash-kpis">
        <KpiCard
          label="Total stock units"
          value={kpis.total_stock.toLocaleString()}
          sub={`${kpis.total_items} inventory lines`}
          accent="#8b5cf6"
        />
        <KpiCard
          label="Low stock alerts"
          value={kpis.low_stock_count}
          sub="≤ 10 units"
          accent={kpis.low_stock_count > 0 ? "#ef4444" : "#10b981"}
        />
        <KpiCard
          label="Total orders"
          value={kpis.total_orders}
          sub={`${kpis.pending_orders_count} pending`}
          accent="#3b82f6"
        />
        <KpiCard
          label="Rack utilization"
          value={`${kpis.overall_rack_percent}%`}
          sub="across all racks"
          accent={kpis.overall_rack_percent >= 80 ? "#ef4444" : kpis.overall_rack_percent >= 50 ? "#f59e0b" : "#10b981"}
        />
      </div>

      {/* ── middle row ── */}
      <div className="dash-mid">

        {/* recent movements */}
        <div className="dash-card dash-movements">
          <SectionHead title="Recent Stock Movements" count={recent_movements.length} />
          {recent_movements.length === 0 ? (
            <p className="dash-empty">No movements recorded yet.</p>
          ) : (
            <ul className="dash-move-list">
              {recent_movements.map((mv, i) => (
                <li key={i} className="dash-move-row">
                  <div className="dash-move-row__left">
                    <MovementTag type={mv.movement_type} />
                    <span className="dash-move-product">{mv.product_name}</span>
                  </div>
                  <div className="dash-move-row__right">
                    <span
                      style={{
                        fontWeight: 700,
                        color: mv.quantity_changed >= 0 ? "#10b981" : "#ef4444",
                      }}
                    >
                      {mv.quantity_changed >= 0 ? "+" : ""}
                      {mv.quantity_changed}
                    </span>
                    <span className="dash-move-date">{mv.movement_date}</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* pending orders */}
        <div className="dash-card dash-pending">
          <SectionHead title="Pending Orders" count={kpis.pending_orders_count} />
          {pending_orders.length === 0 ? (
            <p className="dash-empty">No pending orders.</p>
          ) : (
            <ul className="dash-order-list">
              {pending_orders.map((o) => (
                <li key={o.order_id} className="dash-order-row">
                  <div>
                    <span className="dash-order-num">
                      {o.order_number || `ORD-${String(o.order_id).padStart(6, "0")}`}
                    </span>
                    <span className="dash-order-customer">{o.customer_name}</span>
                  </div>
                  <span className="dash-order-date">{o.order_date}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* ── bottom row ── */}
      <div className="dash-bottom">

        {/* rack utilization */}
        <div className="dash-card dash-racks">
          <SectionHead title="Rack Utilization" />
          {rack_utilization.length === 0 ? (
            <p className="dash-empty">No racks configured.</p>
          ) : (
            <ul className="dash-rack-list">
              {rack_utilization.map((r, i) => (
                <li key={i} className="dash-rack-row">
                  <div className="dash-rack-row__meta">
                    <span className="dash-rack-code">{r.rack_code}</span>
                    <span className="dash-rack-stock">
                      {r.current_stock.toLocaleString()} / {r.capacity.toLocaleString()}
                    </span>
                  </div>
                  <UtilBar percent={r.percent} />
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* aging / low stock combined */}
        <div className="dash-card dash-aging">
          <SectionHead title="Aging Stock (expiring ≤ 30 days)" count={aging_stock.length} />
          {aging_stock.length === 0 ? (
            <p className="dash-empty">No aging stock detected.</p>
          ) : (
            <ul className="dash-aging-list">
              {aging_stock.map((item, i) => (
                <li key={i} className={`dash-aging-row ${item.is_expired ? "is-expired" : ""}`}>
                  <div>
                    <span className="dash-aging-product">{item.product_name}</span>
                    <span className="dash-aging-batch">{item.batch_name} · {item.rack_number}</span>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <span
                      style={{
                        color: item.is_expired ? "#ef4444" : "#f59e0b",
                        fontWeight: 700,
                        fontSize: 12,
                      }}
                    >
                      {item.is_expired ? "EXPIRED" : "Exp " + item.expiry_date}
                    </span>
                    <span className="dash-aging-qty">{item.quantity} units</span>
                  </div>
                </li>
              ))}
            </ul>
          )}

          {/* low stock section below */}
          {low_stock.length > 0 && (
            <>
              <div className="dash-divider" />
              <SectionHead title="Low Stock" count={low_stock.length} />
              <ul className="dash-aging-list">
                {low_stock.map((item, i) => (
                  <li key={i} className="dash-aging-row">
                    <div>
                      <span className="dash-aging-product">{item.product_name}</span>
                      <span className="dash-aging-batch">{item.batch_name} · {item.rack_number}</span>
                    </div>
                    <span style={{ color: "#ef4444", fontWeight: 700, fontSize: 13 }}>
                      {item.quantity} left
                    </span>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  );
}