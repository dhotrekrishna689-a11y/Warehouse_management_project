from database.db_instance import db


from datetime import datetime

class ProductMovement(db.Model):
    __tablename__ = "productmovements"

    product_movement_id = db.Column(
        db.Integer,
        primary_key = True
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
    source_rack_id = db.Column(
            db.Integer,
            
            db.ForeignKey("racks.rack_id")

    )
    destination_rack_id = db.Column(
            db.Integer,
            db.ForeignKey("racks.rack_id")

    )
    quantity = db.Column(
            db.Integer,
            nullable = False

    )
    reason = db.Column(
        db.String(255),
        nullable=False


    )
    user_id = db.Column(
            db.Integer,
            db.ForeignKey("users.user_id"),
            nullable=False

    )
    movement_date = db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.utcnow

    )

    product = db.relationship(

        "Product",
        back_populates = "productmovements"
    )

    batch = db.relationship(
        "Batch",
        back_populates = "productmovements"
    )

    '''
    rack = db.relationship(
        "Rack",

        back_populates = "productmovements"
    )'''


    source_rack = db.relationship(
        "Rack",
        foreign_keys=[source_rack_id],
        back_populates="source_product_movements"
    )

    destination_rack = db.relationship(
        "Rack",
        foreign_keys=[destination_rack_id],
        back_populates="destination_product_movements"
    )

    user = db.relationship(
        "User",
        back_populates = "productmovements"
    )


    def to_dict(self):
        return {
        "product_movement_id": self.product_movement_id,
        "product_id": self.product_id,
        "batch_id": self.batch_id,
        "source_rack_id": self.source_rack_id,
        "destination_rack_id": self.destination_rack_id,
        "quantity": self.quantity,
        "reason": self.reason,
        "user_id": self.user_id,
        "movement_date": self.movement_date
        }
