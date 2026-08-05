from database.db_instance import db


class Rack(db.Model):
    __tablename__ = "racks"

    rack_id = db.Column(
        db.Integer,
        primary_key=True
    )

    rack_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    capacity = db.Column(
        db.Integer,
        nullable=False

    )

    inventories = db.relationship(
    "Inventory",
    back_populates="rack"
    )

    source_product_movements = db.relationship(
            "ProductMovement",
            foreign_keys="ProductMovement.source_rack_id",
            back_populates="source_rack"
    )


    destination_product_movements = db.relationship(
        "ProductMovement",
        foreign_keys="ProductMovement.destination_rack_id",
        back_populates="destination_rack"
    )

    def to_dict(self):
        return 
        {
            "rack_id": self.rack_id,
            "rack_code": self.rack_code,
            "capacity" : self.capacity
        }