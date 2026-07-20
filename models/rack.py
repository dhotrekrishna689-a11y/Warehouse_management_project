from database.db_instance import db


class Rack(db.Model):
    __tablename__ = "racks"

    rack_id = db.Column(
        db.Integer,
        primary_key=True
    )

    rack_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )