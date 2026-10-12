from database.db_instance import db


class Supplier_Order_Preparation_Item(db.Model):

    __tablename__ = "supplier_order_preparation_items"

    preparation_item_id = db.Column(
        db.Integer,
        primary_key=True
    )

    preparation_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "supplier_order_preparations.preparation_id"
        ),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    prepared_quantity = db.Column(
        db.Integer,
        nullable=False
    )

    batch_number = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    manufacturing_date = db.Column(
        db.Date,
        nullable=False
    )

    expiry_date = db.Column(
        db.Date,
        nullable=True
    )

    preparation = db.relationship(
        "Supplier_Order_Preparation",
        back_populates="preparation_items"
    )

    product = db.relationship(
        "Product",
        back_populates="supplier_order_preparation_items"
    )