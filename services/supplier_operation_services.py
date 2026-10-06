from database.db_instance import db

from models.purchase_order import Purchase_Order
from models.purchase_order_item import Purchase_Order_Item

from exceptions.exceptions import(
    Purchase_Order_Not_Found
)


def get_pending_purchase_orders(supplier_id):
    print("Starting a service layear logic:")
    
    purchase_orders = Purchase_Order.query.filter_by(
        supplier_id=supplier_id,
        status="Pending"
    ).all()

    print("Purchase order:", purchase_orders)
    result = []

    for purchase_order in purchase_orders:

        items = []

        for item in purchase_order.purchase_order_items:

            items.append({
                "product_id": item.product_id,
                "ordered_quantity": item.ordered_quantity
            })

        result.append({
            "purchase_order_id": purchase_order.purchase_order_id,
            "purchase_order_number": purchase_order.purchase_order_number,
            "order_date": purchase_order.order_date,
            "status": purchase_order.status,
            "items": items
        })

        

    return result


def get_purchase_order(purchase_order_id):

    purchase_order = Purchase_Order.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if purchase_order is None:
        raise Purchase_Order_Not_Found("Purchase id not exist's")

    items = []

    for item in purchase_order.purchase_order_items:

        items.append({
            "product_id": item.product_id,
            "product_name": item.product.name,
            "ordered_quantity": item.ordered_quantity
        })

    return {
        "purchase_order_id": purchase_order.purchase_order_id,
        "purchase_order_number": purchase_order.purchase_order_number,
        "supplier_id": purchase_order.supplier_id,
        "order_date": purchase_order.order_date,
        "status": purchase_order.status,
        "items": items
    }