from database.db_instance import db


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
        db.String(100),
        nullable=False
    )

    movement_date = db.Column(
        db.Date,
        nullable=False
    )

    inventory = db.relationship(
    "Inventory",
    back_populates="stock_movements"
    )

    user = db.relationship(
    "User",
    back_populates="stock_movements"
    )