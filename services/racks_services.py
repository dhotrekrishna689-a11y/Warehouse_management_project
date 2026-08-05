from database.db_instance import db
from models.rack import Rack
from models.inventory import Inventory

def create_rack(rack_code):

    if not rack_code:
        return "empty_rack_code"

    existing_rack = Rack.query.filter_by(
        rack_code=rack_code
    ).first()

    if existing_rack:
        return "duplicate_rack"

    rack = Rack(
        rack_code=rack_code
    )

    db.session.add(rack)
    db.session.commit()

    return rack

def get_racks():

    racks = Rack.query.all()

    return racks

def get_specific_rack(rack_id):

    rack = db.session.get(Rack, rack_id)

    if rack is None:
        return None

    return rack

def update_rack(rack_id, rack_code):

    rack = db.session.get(Rack, rack_id)

    if rack is None:
        return None

    if not rack_code:
        return "empty_rack_code"

    existing_rack = Rack.query.filter_by(
        rack_code=rack_code
    ).first()

    if existing_rack:

        if existing_rack.rack_id != rack_id:
            return "duplicate_rack"

    rack.rack_code = rack_code

    db.session.commit()

    return rack




def delete_rack(rack_id):

    rack = db.session.get(Rack, rack_id)

    if rack is None:
        return None

    inventory = Inventory.query.filter_by(
        rack_id=rack_id
    ).first()

    if inventory:
        return "rack_in_use"

    db.session.delete(rack)
    db.session.commit()

    return rack




def get_rack_utilization():

    racks = Rack.query.all()

    rack_utilization = []

    for rack in racks:

        current_stock = 0

        for inventory in rack.inventories:
            current_stock += inventory.quantity

        if rack.capacity == 0:
            utilization_percentage = 0
        else:
            utilization_percentage = (
                current_stock / rack.capacity
            ) * 100

        rack_utilization.append({
            "rack_id": rack.rack_id,
            "rack_code": rack.rack_code,
            "capacity": rack.capacity,
            "current_stock": current_stock,
            "utilization_percentage": round(utilization_percentage, 2)
        })

    return rack_utilization