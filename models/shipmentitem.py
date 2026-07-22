from database.db_instance import db


class ShipmentItem(db.Model):
    __tablename__ = "shipment_items"

    shipment_item_id = db.Column(
        db.Integer,
        primary_key=True
    )

    shipment_id = db.Column(
        db.Integer,
        db.ForeignKey("shipments.shipment_id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey("batches.batch_id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )