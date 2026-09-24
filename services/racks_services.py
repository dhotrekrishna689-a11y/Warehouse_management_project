from database.db_instance import db
from models.rack import Rack
from models.inventory import Inventory
from exceptions.exceptions import (
    Rack_Not_Found_Error,
    Rack_Duplicate_Found_Error,
    Rack_Cannot_Delete,
    Empty_Field_Error,
)


def create_rack(rack_code, capacity):

    if not rack_code:
        raise Empty_Field_Error("Rack code is required")

    if capacity is None:
        raise Empty_Field_Error("Rack capacity is required")

    existing_rack = Rack.query.filter_by(rack_code=rack_code).first()
    if existing_rack:
        raise Rack_Duplicate_Found_Error("A rack with this code already exists")

    rack = Rack(rack_code=rack_code, capacity=capacity)

    try:
        db.session.add(rack)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return rack


def get_racks():
    return Rack.query.all()


def get_specific_rack(rack_id):
    rack = db.session.get(Rack, rack_id)
    if rack is None:
        raise Rack_Not_Found_Error("Rack not found")
    return rack


def update_rack(rack_id, rack_code):

    rack = db.session.get(Rack, rack_id)
    if rack is None:
        raise Rack_Not_Found_Error("Rack not found")

    if not rack_code:
        raise Empty_Field_Error("Rack code is required")

    existing_rack = Rack.query.filter_by(rack_code=rack_code).first()
    if existing_rack and existing_rack.rack_id != rack_id:
        raise Rack_Duplicate_Found_Error("A rack with this code already exists")

    rack.rack_code = rack_code

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return rack


def delete_rack(rack_id):

    rack = db.session.get(Rack, rack_id)
    if rack is None:
        raise Rack_Not_Found_Error("Rack not found")

    inventory = Inventory.query.filter_by(rack_id=rack_id).first()
    if inventory:
        raise Rack_Cannot_Delete(
            "Cannot delete rack because inventory is stored in it"
        )

    try:
        db.session.delete(rack)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return rack


def get_rack_utilization():

    racks = Rack.query.all()
    rack_utilization = []

    for rack in racks:
        current_stock = sum(inv.quantity for inv in rack.inventories)
        capacity = rack.capacity or 0
        utilization_percentage = (
            round((current_stock / capacity) * 100, 2) if capacity else 0
        )
        rack_utilization.append({
            "rack_id":               rack.rack_id,
            "rack_code":             rack.rack_code,
            "capacity":              capacity,
            "current_stock":         current_stock,
            "utilization_percentage": utilization_percentage,
        })

    return rack_utilization