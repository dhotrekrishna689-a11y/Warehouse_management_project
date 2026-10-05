from database.db_instance import db

class Supplier(db.Model):

    __tablename__ = "suppliers"

    supplier_id = db.Column(
            db.Integer,
            primary_key = True
    )

    supplier_name = db.Column(
            db.String(100),
            nullable = False
    )

    purchase_orders = db.relationship(
    "Purchase_Order",
    back_populates="supplier"
   )