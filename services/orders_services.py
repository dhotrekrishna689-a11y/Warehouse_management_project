from database.db_instance import db
from models.order import Order
from models.orderitem import OrderItem
from models.inventory import Inventory


'''
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
'''

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





def create_order(order_data):

    # ------------------------
    # Order Level Validation
    # ------------------------

    customer_name = order_data.get("customer_name")
    order_date = order_data.get("order_date")
    items = order_data.get("items")

    if not customer_name:
        return "Customer name is required."

    if not order_date:
        return "Order date is required."

    if not items:
        return "Order must contain at least one item."

    # ------------------------
    # Item Level Validation
    # ------------------------

    for index, item in enumerate(items, start=1):

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if not product_id:
            return f"Product is required for item {index}."

        if quantity is None:
            return f"Quantity is required for item {index}."

        if quantity <= 0:
            return f"Quantity must be greater than zero for item {index}."

    # ------------------------
    # Create Order
    # ------------------------

    order = Order(
        customer_name=customer_name,
        order_date=order_date
    )

    db.session.add(order)

    db.session.flush()

    order.order_number = f"ORD-{order.order_id:06d}"

    # ------------------------
    # Create Order Items
    # ------------------------

    for item in items:

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        order_item = OrderItem(
            order_id=order.order_id,
            product_id=product_id,
            quantity=quantity
        )

        db.session.add(order_item)

    # ------------------------
    # Commit
    # ------------------------

    db.session.commit()

    return order


def get_pick_list(order_id):
    print("===== PICK LIST SERVICE CALLED =====")
    print("ORDER ID:", order_id)

    order = Order.query.get(order_id)

    if not order:
        return "Order not found."

    pick_list = []

    for order_item in order.order_items:

        need_quantity = order_item.quantity

        inventories = Inventory.query.filter_by(
            product_id=order_item.product_id
        ).all()


        total_available = sum(
        inventory.quantity
        for inventory in inventories
        )

        print("Product:", order_item.product_id)
        print("Need:", need_quantity)
        print("Available:", total_available)

        if not inventories:
            return f"No inventory found for Product ID {order_item.product_id}"

        # Aage validation aur allocation yahin hoga
        #for order_item in order.order_items:
        #print(order_item.product_id)
        #print(order_item.quantity)

        if total_available < need_quantity:
            return {
            "message": "Insufficient stock.",
            "product_id": order_item.product_id,
            "required": need_quantity,
            "available": total_available
        }, 400



        inventories.sort(
            key=lambda inventory: inventory.batch.expiry_date
        )
        '''
        for inventory in inventories:
            print(
                "Inventory ID:", inventory.inventory_id,
                "Batch ID:", inventory.batch_id,
                "Rack ID:", inventory.rack_id,
                "Quantity:", inventory.quantity
            )'''
        remaining_need = need_quantity
        for inventory in inventories:

            if remaining_need == 0:
                break

            pick_quantity = min(
            remaining_need,
            inventory.quantity
            )

            if pick_quantity > 0:

                pick_list.append({
                "product_id": inventory.product_id,
                "batch_id": inventory.batch_id,
                "rack_id": inventory.rack_id,
                "pick_quantity": pick_quantity
            })

            remaining_need -= pick_quantity

    return {
        "order_id": order.order_id,
        "order_number": order.order_number,
        "customer_name": order.customer_name,
        "items": pick_list
    }