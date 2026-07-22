from database.db_instance import db


class Shipment(db.Model):
    __tablename__ = "shipments"

    shipment_id = db.Column(
        db.Integer,
        primary_key=True
    )

    shipment_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    received_date = db.Column(
        db.Date,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    user = db.relationship(
    "User",
    back_populates="shipments"
    )