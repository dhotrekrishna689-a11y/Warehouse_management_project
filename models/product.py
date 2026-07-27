from database.db_instance import db

class Product(db.Model):

    __tablename__ = "products"


    product_id = db.Column(
                                db.Integer,
                                primary_key = True
                          )
    
    category_id = db.Column(
                                db.Integer,
                                db.ForeignKey("categories.category_id"),

                           )
    
    name = db.Column(
                        db.String(100),
                        nullable = False
    )

    sku = db.Column(
                        db.String(100),
                        unique = True,
                        nullable = False

    )

    description = db.Column(
                                db.String(100),
                                nullable = True
    )

    #category = db.relationship("Category")

    category = db.relationship(
    "Category",
    back_populates="products"
    )

    batches = db.relationship(
    "Batch",
    back_populates="product"
    )

    inventories = db.relationship(
    "Inventory",
    back_populates="product"
    )

    shipment_items = db.relationship(
    "ShipmentItem",
    back_populates="product"
    )

    order_items = db.relationship(
    "OrderItem",
    back_populates="product"
    )


    def to_dict(self):
        return {
            "product_id": self.product_id,
            "category_id": self.category_id,
            "name": self.name,
            "sku": self.sku,
            "description": self.description
        }