from database.db_instance import db
from sqlalchemy import Enum


class Supplier_Order_Preparation(db.Model):

    __tablename__ = "supplier_order_preparations"

    preparation_id = db.Column(
        db.Integer,
        primary_key=True
    )

    purchase_order_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_orders.purchase_order_id"),
        unique=True,
        nullable=False
    )

    expected_dispatch_date = db.Column(
        db.Date,
        nullable=True
    )

    expected_delivery_date = db.Column(
        db.Date,
        nullable=True
    )

    shipment_number = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    status = db.Column(
        Enum(
            "Pending",
            "Prepared",
            "Confirmed",
            name = "supplier_order_preparation_item"
        ),
        nullable=False,
        default="Pending"
    )

    purchase_order = db.relationship(
        "Purchase_Order",
        back_populates="supplier_order_preparation"
    )

    preparation_items = db.relationship(
        "Supplier_Order_Preparation_Item",
        back_populates="preparation",
        cascade="all, delete-orphan"
    )