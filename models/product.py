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