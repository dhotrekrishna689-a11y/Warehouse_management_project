from database.db_instance import db
from models.shipment import Shipment
from models.shipmentitem import ShipmentItem
from models.user import User


def create_shipment(
    shipment_number,
    received_date,
    user_id
):

    if not shipment_number:
        return "empty_shipment_number"

    existing_shipment = Shipment.query.filter_by(
        shipment_number=shipment_number
    ).first()

    if existing_shipment:
        return "duplicate_shipment"

    user = db.session.get(User, user_id)

    if user is None:
        return "user_not_found"

    shipment = Shipment(
        shipment_number=shipment_number,
        received_date=received_date,
        user_id=user_id
    )

    db.session.add(shipment)
    db.session.commit()

    return shipment

def get_shipments():

    shipments = Shipment.query.all()

    return shipments

def get_specific_shipment(shipment_id):

    shipment = db.session.get(Shipment, shipment_id)

    if shipment is None:
        return None

    return shipment

def update_shipment(
    shipment_id,
    shipment_number,
    received_date,
    user_id
):

    shipment = db.session.get(Shipment, shipment_id)

    if shipment is None:
        return None

    if not shipment_number:
        return "empty_shipment_number"

    existing_shipment = Shipment.query.filter_by(
        shipment_number=shipment_number
    ).first()

    if existing_shipment:

        if existing_shipment.shipment_id != shipment_id:
            return "duplicate_shipment"

    user = db.session.get(User, user_id)

    if user is None:
        return "user_not_found"

    shipment.shipment_number = shipment_number
    shipment.received_date = received_date
    shipment.user_id = user_id

    db.session.commit()

    return shipment




def delete_shipment(shipment_id):

    shipment = db.session.get(Shipment, shipment_id)

    if shipment is None:
        return None

    shipment_item = ShipmentItem.query.filter_by(
        shipment_id=shipment_id
    ).first()

    if shipment_item:
        return "shipment_in_use"

    db.session.delete(shipment)
    db.session.commit()

    return shipment