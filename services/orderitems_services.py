from database.db_instance import db
from models.order import Order
from models.product import Product
from models.orderitem import OrderItem


from exceptions.exceptions import (
    Validation_Error,
    Order_Not_Found_Error,
    Product_Not_Found_Error,
    Order_Item_Not_Found_Error,
    Order_Item_Duplicate_Found_Error
)
'''

def create_order_item(
    order_id,
    product_id,
    quantity
):

    if not order_id:
        return "empty_order_id"

    if not product_id:
        return "empty_product_id"

    if not quantity:
        return "empty_quantity"

    order = db.session.get(
        Order,
        order_id
    )

    if order is None:
        return "order_not_found"

    product = db.session.get(
        Product,
        product_id
    )

    if product is None:
        return "product_not_found"

    existing_order_item = OrderItem.query.filter_by(
        order_id=order_id,
        product_id=product_id
    ).first()

    print("Existing order item:", existing_order_item)

    if existing_order_item:
        return "duplicate_order_item"

    order_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity
    )

    db.session.add(order_item)
    db.session.commit()

    return order_item

def get_order_items():

    order_items = OrderItem.query.all()

    return order_items

def get_specific_order_item(order_item_id):

    order_item = db.session.get(
        OrderItem,
        order_item_id
    )

    if order_item is None:
        return None

    return order_item

def update_order_item(
    order_item_id,
    quantity
):

    order_item = db.session.get(
        OrderItem,
        order_item_id
    )

    if order_item is None:
        return None

    if quantity is None:
        return "empty_quantity"

    if quantity <= 0:
        return "invalid_quantity"

    order_item.quantity = quantity

    db.session.commit()

    return order_item

def delete_order_item(order_item_id):

    order_item = db.session.get(
        OrderItem,
        order_item_id
    )

    if order_item is None:
        return None

    db.session.delete(order_item)
    db.session.commit()

    return order_item'''

def create_order_item(
    order_id,
    product_id,
    quantity
):

    if not order_id:
        raise Validation_Error("Order ID is required")

    if not product_id:
        raise Validation_Error("Product ID is required")

    if not quantity:
        raise Validation_Error("Quantity is required")

    order = db.session.get(
        Order,
        order_id
    )

    if order is None:
        raise Order_Not_Found_Error("Order Not Found")

    product = db.session.get(
        Product,
        product_id
    )

    if product is None:
        raise Product_Not_Found_Error("Product Not Found")

    existing_order_item = OrderItem.query.filter_by(
        order_id=order_id,
        product_id=product_id
    ).first()

    if existing_order_item:
        raise Order_Item_Duplicate_Found_Error(
            "Order item already exists for this order"
        )

    order_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity
    )

    try:
        db.session.add(order_item)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return order_item


def get_order_items():

    order_items = OrderItem.query.all()

    return order_items


def get_specific_order_item(order_item_id):

    order_item = db.session.get(
        OrderItem,
        order_item_id
    )

    if order_item is None:
        raise Order_Item_Not_Found_Error(
            "Order Item Not Found"
        )

    return order_item


def update_order_item(
    order_item_id,
    quantity
):

    order_item = db.session.get(
        OrderItem,
        order_item_id
    )

    if order_item is None:
        raise Order_Item_Not_Found_Error(
            "Order Item Not Found"
        )

    if quantity is None:
        raise Validation_Error(
            "Quantity is required"
        )

    if quantity <= 0:
        raise Validation_Error(
            "Quantity must be greater than zero"
        )

    order_item.quantity = quantity

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return order_item


def delete_order_item(order_item_id):

    order_item = db.session.get(
        OrderItem,
        order_item_id
    )

    if order_item is None:
        raise Order_Item_Not_Found_Error(
            "Order Item Not Found"
        )

    try:
        db.session.delete(order_item)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return order_item