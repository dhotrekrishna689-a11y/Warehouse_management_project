from database.db_instance import  db

class Purchase_Order_Item(db.Model):

    __tablename__= "purchase_order_items"

    poi_id= db.Column(
        db.Integer,
        primary_key = True

    )

    purchase_order_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_orders.purchase_order_id"),
        nullable = False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable = False
    )

    ordered_quantity = db.Column(
        db.Integer,
        nullable = False
    )

   

    purchase_order = db.relationship(
        "Purchase_Order",
        back_populates="purchase_order_items"
    )

    # Purchase Order Item → Product
    product = db.relationship(
        "Product",
        back_populates="purchase_order_items"
    )

    