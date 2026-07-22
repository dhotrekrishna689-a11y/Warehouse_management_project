from database.db_instance import db


class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    order_date = db.Column(
        db.Date,
        nullable=False
    )

    order_items = db.relationship(
    "OrderItem",
    back_populates="order"
    )