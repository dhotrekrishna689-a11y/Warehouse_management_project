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

    stock_movements = db.relationship(
    "StockMovement",
    back_populates="inventory"
    )

    def to_dict(self):
        return {
        "inventory_id": self.inventory_id,
        "product_id": self.product_id,
        "batch_id": self.batch_id,
        "rack_id": self.rack_id,
        "quantity": self.quantity
        }

    __table_args__ = (
    db.UniqueConstraint(
        "product_id",
        "batch_id",
        "rack_id",
        name="uq_inventory_product_batch_rack"
        ),
    )

    
