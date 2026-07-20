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
                        db.Integer,
                        unique = True,
                        nullable = False

    )

    description = db.Column(
                                db.String(100),
                                nullable = True
    )

    category = db.relationship("categories")