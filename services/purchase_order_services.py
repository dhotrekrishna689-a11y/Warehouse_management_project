from database.db_instance import db
from models.purchase_order import Purchase_Order
from models.purchase_order_item import Purchase_Order_Item

from exceptions.exceptions import(
    Supplier_Not_Found, 
    Product_Not_Found_Error
)

'''
def purchase_order(supplier_id, items):

    # Looking for Wether Supplier is Enter/Not
    supplier_id =
    if supplier_id is None:
        raise Supplier_Not_Found("Supplier Doesn't Exist's")

    #Looking for wether product is Empty/Not
    if items is None:
        raise Product_Not_Found_Error("User not enters the product")

    #Looking nam
    for item in items:
        if item["name"] is None:
            raise Product_Not_Found_Error("Product not found")
        elif item["quantity"] is None or item["quantity"] <+ 0:
'''

from database.db_instance import db
from models.purchase_order import Purchase_Order
from models.purchase_order_item import Purchase_Order_Item
from models.supplier import Supplier
from models.product import Product

from datetime import datetime

from exceptions.exceptions import (
    Supplier_Not_Found,
    Product_Not_Found_Error
)


def purchase_order(supplier_id, items):

    # 1. Supplier ID check
    if supplier_id is None:
        raise Supplier_Not_Found(
            "Supplier ID is required"
        )

    # 2. Supplier exists in database?
    supplier = Supplier.query.filter_by(
        supplier_id=supplier_id
    ).first()

    if supplier is None:
        raise Supplier_Not_Found(
            "Supplier doesn't exist"
        )

    # 3. Items check
    if not items:
        raise Product_Not_Found_Error(
            "No products entered"
        )

    # 4. Merge same products
    merged_items = {}

    for item in items:

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        # Product ID validation
        if product_id is None:
            raise Product_Not_Found_Error(
                "Product ID is required"
            )

        # Quantity validation
        if quantity is None or quantity <= 0:
            raise Product_Not_Found_Error(
                "Quantity must be greater than 0"
            )

        # Product exists?
        product = Product.query.filter_by(
            product_id=product_id
        ).first()

        if product is None:
            raise Product_Not_Found_Error(
                f"Product {product_id} doesn't exist"
            )

        # Merge duplicate product
        if product_id in merged_items:
            merged_items[product_id] += quantity
        else:
            merged_items[product_id] = quantity

    # 5. Generate Purchase Order Number
    last_po = Purchase_Order.query.order_by(
        Purchase_Order.purchase_order_id.desc()
    ).first()

    if last_po:
        next_id = last_po.purchase_order_id + 1
    else:
        next_id = 1

    purchase_order_number = f"PO-{next_id:06d}"

    # 6. Create Purchase Order
    purchase_order = Purchase_Order(
        purchase_order_number=purchase_order_number,
        supplier_id=supplier_id,
        order_date=datetime.utcnow(),
        status="Pending"
    )

    db.session.add(purchase_order)

    # Flush so purchase_order_id becomes available
    db.session.flush()

    # 7. Create Purchase Order Items
    for product_id, quantity in merged_items.items():

        purchase_order_item = Purchase_Order_Item(
            purchase_order_id=purchase_order.purchase_order_id,
            product_id=product_id,
            ordered_quantity=quantity
        )

        db.session.add(purchase_order_item)

    # 8. Save everything
    db.session.commit()

    return {
        "purchase_order_id": purchase_order.purchase_order_id,
        "purchase_order_number": purchase_order.purchase_order_number,
        "supplier_id": purchase_order.supplier_id,
        "status": purchase_order.status
    }

