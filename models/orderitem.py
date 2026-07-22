from database.db_instance import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    order_item_id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.order_id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )