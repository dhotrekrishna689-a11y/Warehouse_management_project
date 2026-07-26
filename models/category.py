from database.db_instance import db

class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(
                                db.Integer, 
                                primary_key = True
                            )

    name = db.Column(
                        db.String(100),
                        nullable = False,
                        unique = True

    )
    
    products = db.relationship(
    "Product",
    back_populates="category"
    )
    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name
        }