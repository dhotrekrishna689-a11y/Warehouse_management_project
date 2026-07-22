from database.db_instance import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    hashed_password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False
    )

    shipments = db.relationship(
    "Shipment",
    back_populates="user"
    )

    stock_movements = db.relationship(
    "StockMovement",
    back_populates="user"
    )
