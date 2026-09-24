from database.db_instance import db
from models.order import Order
from models.orderitem import OrderItem
from models.inventory import Inventory
from models.stockmovement import StockMovement
import datetime
from exceptions.exceptions import (
    Order_Not_Found_Error,
    Order_Cannot_Delete,
    Validation_Error,
    Qunatity_validation_Error,
    Empty_Field_Error,
    Inventory_Not_Found_Error,
)


def get_orders():
    return Order.query.all()


def get_specific_order(order_id):
    order = db.session.get(Order, order_id)
    if order is None:
        raise Order_Not_Found_Error("Order not found")
    return order


def update_order(order_id, order_date):

    order = db.session.get(Order, order_id)
    if order is None:
        raise Order_Not_Found_Error("Order not found")

    if not order_date:
        raise Empty_Field_Error("Order date is required")

    order.order_date = order_date

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return order


def delete_order(order_id):

    order = db.session.get(Order, order_id)
    if order is None:
        raise Order_Not_Found_Error("Order not found")

    if len(order.order_items) > 0:
        raise Order_Cannot_Delete(
            "Cannot delete order because it contains order items"
        )

    try:
        db.session.delete(order)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return order


def create_order(order_data):

    customer_name = order_data.get("customer_name")
    order_date    = order_data.get("order_date")
    items         = order_data.get("items")

    if not customer_name:
        raise Empty_Field_Error("Customer name is required")

    if not order_date:
        raise Empty_Field_Error("Order date is required")

    if not items:
        raise Validation_Error("Order must contain at least one item")

    for index, item in enumerate(items, start=1):
        product_id = item.get("product_id")
        quantity   = item.get("quantity")

        if not product_id:
            raise Empty_Field_Error(f"Product is required for item {index}")

        if quantity is None:
            raise Empty_Field_Error(f"Quantity is required for item {index}")

        if quantity <= 0:
            raise Qunatity_validation_Error(
                f"Quantity must be greater than zero for item {index}"
            )

    # Parse date string → date object
    if isinstance(order_date, str):
        try:
            order_date = datetime.date.fromisoformat(order_date)
        except ValueError:
            raise Validation_Error("Invalid order date format. Use YYYY-MM-DD")

    order = Order(
        customer_name=customer_name,
        order_date=order_date,
        status="PENDING"
    )

    db.session.add(order)
    db.session.flush()
    order.order_number = f"ORD-{order.order_id:06d}"

    for item in items:
        order_item = OrderItem(
            order_id=order.order_id,
            product_id=item.get("product_id"),
            quantity=item.get("quantity")
        )
        db.session.add(order_item)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return order


def get_pick_list(order_id):

    order = Order.query.get(order_id)
    if not order:
        raise Order_Not_Found_Error("Order not found")

    if order.status == "DISPATCHED":
        return {
            "message": "This order has already been dispatched.",
            "status": "DISPATCHED",
            "order_id": order.order_id,
            "order_number": order.order_number,
        }, 400

    pick_list = []

    for order_item in order.order_items:
        need_quantity = order_item.quantity

        inventories = Inventory.query.filter_by(
            product_id=order_item.product_id
        ).all()

        if not inventories:
            return {
                "message": f"No inventory found for Product ID {order_item.product_id}",
                "status": "OUT_OF_STOCK",
            }, 400

        total_available = sum(inv.quantity for inv in inventories)

        if total_available < need_quantity:
            return {
                "message": "Insufficient stock.",
                "status": "OUT_OF_STOCK",
                "product_id": order_item.product_id,
                "required": need_quantity,
                "available": total_available,
            }, 400

        inventories.sort(key=lambda inv: inv.batch.expiry_date)

        remaining_need = need_quantity
        for inventory in inventories:
            if remaining_need == 0:
                break

            pick_quantity = min(remaining_need, inventory.quantity)

            if pick_quantity > 0:
                pick_list.append({
                    "inventory_id": inventory.inventory_id,
                    "product_id":   inventory.product_id,
                    "batch_id":     inventory.batch_id,
                    "rack_id":      inventory.rack_id,
                    "pick_quantity": pick_quantity,
                })

            remaining_need -= pick_quantity

    return {
        "order_id":      order.order_id,
        "order_number":  order.order_number,
        "customer_name": order.customer_name,
        "items":         pick_list,
    }


def update_inventory_after_pick(order_id, items):

    order = Order.query.get(order_id)
    if not order:
        raise Order_Not_Found_Error("Order not found")

    if not items:
        raise Validation_Error("No picked items provided")

    picked_items = []

    for item in items:
        inventory_id  = item.get("inventory_id")
        pick_quantity = item.get("quantity")

        if not inventory_id or not pick_quantity:
            raise Validation_Error("inventory_id and quantity are required for each item")

        inventory = Inventory.query.get(inventory_id)
        if not inventory:
            raise Inventory_Not_Found_Error(f"Inventory {inventory_id} not found")

        if inventory.quantity < pick_quantity:
            raise Qunatity_validation_Error(
                f"Insufficient stock for inventory {inventory_id}. "
                f"Available: {inventory.quantity}, Requested: {pick_quantity}"
            )

        inventory.quantity -= pick_quantity

        movement = StockMovement(
            inventory_id=inventory.inventory_id,
            user_id=1,
            quantity_changed=-pick_quantity,
            movement_type="PICKED",
            reason=f"Order picking - Order {order.order_id}"
        )
        db.session.add(movement)

        picked_items.append({
            "inventory_id":     inventory.inventory_id,
            "picked_quantity":  pick_quantity,
            "remaining_quantity": inventory.quantity
        })

    order.status = "DISPATCHED"

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "message": "Inventory updated successfully after picking.",
        "order_id": order.order_id,
        "picked_items": picked_items
    }, 200