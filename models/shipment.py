from database.db_instance import db


class Shipment(db.Model):
    __tablename__ = "shipments"

    shipment_id = db.Column(
        db.Integer,
        primary_key=True
    )

    shipment_number = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    received_date = db.Column(
        db.Date,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )


    purchase_order_id = db.Column(
    db.Integer,
    db.ForeignKey("purchase_orders.purchase_order_id"),
    unique=True,
    nullable=False
    )

    user = db.relationship(
    "User",
    back_populates="shipments"
    )

    shipment_items = db.relationship(
    "ShipmentItem",
    back_populates="shipment"
    )

    purchase_order = db.relationship(
    "Purchase_Order",
    back_populates="shipments"
    )

    def to_dict(self):
        return {
        "shipment_id": self.shipment_id,
        "shipment_number": self.shipment_number,
        "received_date": self.received_date,
        "user_id": self.user_id
        }