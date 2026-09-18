from datetime import date, timedelta
from database.db_instance import db
from models.inventory import Inventory
from models.order import Order
from models.rack import Rack
from models.stockmovement import StockMovement


def get_dashboard_data():

    # ─── 1. KPI CARDS ───────────────────────────────────────────────────────────

    inventories = Inventory.query.all()

    total_stock   = sum(inv.quantity for inv in inventories)
    total_items   = len(inventories)

    LOW_STOCK_THRESHOLD = 10
    low_stock_items = [
        {
            "product_name": inv.product.name,
            "batch_name":   inv.batch.batch_number,
            "rack_number":  inv.rack.rack_code,
            "quantity":     inv.quantity,
        }
        for inv in inventories
        if inv.quantity <= LOW_STOCK_THRESHOLD
    ]

    orders          = Order.query.all()
    total_orders    = len(orders)
    pending_orders  = [o for o in orders if (o.status or "PENDING") == "PENDING"]

    # ─── 2. PENDING ORDERS (latest 5) ───────────────────────────────────────────

    pending_orders_data = [
        {
            "order_id":      o.order_id,
            "order_number":  o.order_number,
            "customer_name": o.customer_name,
            "order_date":    str(o.order_date) if o.order_date else None,
            "status":        o.status or "PENDING",
        }
        for o in sorted(pending_orders, key=lambda x: x.order_id, reverse=True)[:5]
    ]

    # ─── 3. RACK UTILIZATION ────────────────────────────────────────────────────

    racks = Rack.query.all()
    rack_utilization = []
    for rack in racks:
        current_stock = sum(inv.quantity for inv in rack.inventories)
        capacity      = rack.capacity or 0
        percent       = round((current_stock / capacity * 100), 1) if capacity else 0
        rack_utilization.append({
            "rack_code":    rack.rack_code,
            "capacity":     capacity,
            "current_stock": current_stock,
            "percent":      percent,
        })

    total_capacity  = sum(r["capacity"]      for r in rack_utilization)
    total_used      = sum(r["current_stock"] for r in rack_utilization)
    overall_percent = round((total_used / total_capacity * 100), 1) if total_capacity else 0

    # ─── 4. AGING STOCK (expiry within 30 days or already expired) ──────────────

    today     = date.today()
    soon      = today + timedelta(days=30)
    aging = []
    for inv in inventories:
        expiry = inv.batch.expiry_date if inv.batch else None
        if expiry and expiry <= soon:
            aging.append({
                "product_name": inv.product.name,
                "batch_name":   inv.batch.batch_number,
                "rack_number":  inv.rack.rack_code,
                "quantity":     inv.quantity,
                "expiry_date":  str(expiry),
                "is_expired":   expiry < today,
            })
    aging.sort(key=lambda x: x["expiry_date"])

    # ─── 5. RECENT STOCK MOVEMENTS (latest 8) ───────────────────────────────────

    recent_movements = (
        StockMovement.query
        .order_by(StockMovement.movement_date.desc())
        .limit(8)
        .all()
    )
    movements_data = []
    for mv in recent_movements:
        inv = mv.inventory
        movements_data.append({
            "product_name":    inv.product.name  if inv else "—",
            "movement_type":   mv.movement_type,
            "quantity_changed": mv.quantity_changed,
            "reason":          mv.reason,
            "movement_date":   mv.movement_date.strftime("%Y-%m-%d %H:%M") if mv.movement_date else None,
        })

    return {
        "kpis": {
            "total_stock":           total_stock,
            "total_items":           total_items,
            "low_stock_count":       len(low_stock_items),
            "total_orders":          total_orders,
            "pending_orders_count":  len(pending_orders),
            "overall_rack_percent":  overall_percent,
        },
        "low_stock":          low_stock_items[:6],
        "pending_orders":     pending_orders_data,
        "rack_utilization":   rack_utilization,
        "aging_stock":        aging[:6],
        "recent_movements":   movements_data,
    }
