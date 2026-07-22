from database.db_instance import db


class Batch(db.Model):
    __tablename__ = "batches"

    batch_id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    batch_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    manufacturing_date = db.Column(
        db.Date,
        nullable=False
    )

    expiry_date = db.Column(
        db.Date,
        nullable=True
    )

    #product = db.relationship("Product")

    product = db.relationship(
    "Product",
    back_populates="batches"
    )

    inventory = db.relationship(
    "Inventory",
    back_populates="batch",
    uselist=False
    )

    shipment_items = db.relationship(
    "ShipmentItem",
    back_populates="batch"
    )