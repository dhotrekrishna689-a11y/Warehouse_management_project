from database.db_instance import  db
from datetime import datetime
from sqlalchemy import Enum

class Purchase_Order(db.Model):

    __tablename__ = "purchase_orders"

    purchase_order_id = db.Column(
                db.Integer,
                primary_key = True
    )

    purchase_order_number = db.Column(
                db.String(100),
                unique = True,
                nullable = False

    )

    supplier_id = db.Column(
            db.Integer,
            db.ForeignKey("suppliers.supplier_id"),
            nullable = False
    )

    order_date = db.Column(
        db.DateTime,
        nullable = False
    )

    status = db.Column(
        Enum(
            "Pending",
            "Prepared",
            name = "purchase_order_enum"
        ),
        nullable = False

    )

    purchase_order_items = db.relationship(
        "Purchase_Order_Item",
        back_populates = "purchase_order"
    )

    shipments = db.relationship(
        "Shipment",
        back_populates="purchase_order"
    )

    # Purchase Order → Supplier
    supplier = db.relationship(
        "Supplier",
        back_populates="purchase_orders"
    )