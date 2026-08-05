from database.db_instance import db
from datetime import datetime
from sqlalchemy import Enum

class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    stock_movement_id = db.Column(
        db.Integer,
        primary_key=True
    )

    inventory_id = db.Column(
        db.Integer,
        db.ForeignKey("inventory.inventory_id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    quantity_changed = db.Column(
        db.Integer,
        nullable=False
    )

    movement_type = db.Column(
        Enum(
            "RECEIVED",
            "DISPATCHED",
            "ADJUSTMENT",
            "MOVED_OUT",
            "MOVED_IN",
            name="movement_type_enum"
        ),
        nullable=False
    )


    reason = db.Column(
        db.String(255),
        nullable=False
    )

    movement_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    inventory = db.relationship(
    "Inventory",
    back_populates="stock_movements"
    )

    user = db.relationship(
    "User",
    back_populates="stock_movements"
    )