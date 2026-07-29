from database.db_instance import db
from models.order import Order


def create_order(
    order_number,
    order_date
):

    if not order_number:
        return "empty_order_number"

    if not order_date:
        return "empty_order_date"

    existing_order = Order.query.filter_by(
        order_number=order_number
    ).first()

    if existing_order:
        return "duplicate_order"

    order = Order(
        order_number=order_number,
        order_date=order_date
    )

    db.session.add(order)
    db.session.commit()

    return order


def get_orders():

    orders = Order.query.all()

    return orders


def get_specific_order(order_id):

    order = db.session.get(
        Order,
        order_id
    )

    if order is None:
        return None

    return order

def update_order(
    order_id,
    order_date
):

    order = db.session.get(
        Order,
        order_id
    )

    if order is None:
        return None

    if not order_date:
        return "empty_order_date"

    order.order_date = order_date

    db.session.commit()

    return order

def delete_order(order_id):

    order = db.session.get(
        Order,
        order_id
    )

    if order is None:
        return None

    if len(order.order_items) > 0:
        return "order_has_items"

    db.session.delete(order)
    db.session.commit()

    return order