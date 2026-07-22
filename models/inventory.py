from database.db_instance import db


class Inventory(db.Model):
    __tablename__ = "inventory"

    inventory_id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey("batches.batch_id"),
        unique=True,
        nullable=False
    )

    rack_id = db.Column(
        db.Integer,
        db.ForeignKey("racks.rack_id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    product = db.relationship(
    "Product",
    back_populates="inventories"
    )

    rack = db.relationship(
    "Rack",
    back_populates="inventories"
    )
    
    batch = db.relationship(
    "Batch",
    back_populates="inventory"
    )
