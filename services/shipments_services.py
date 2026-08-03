from database.db_instance import db
from models.shipment import Shipment
from models.shipmentitem import ShipmentItem
from models.user import User
from services.inventory_operations import apply_stock_movement
from models.inventory import Inventory
from models.product import Product
from models.batch import Batch
from models.rack import Rack


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


def receive_shipment(shipment_data):
     # Shipment Level Validation

    received_date = shipment_data.get("received_date")
    items = shipment_data.get("items")

    if not received_date:
        return "Received date is required."

    if not items:
        return "Shipment must contain at least one item."

    # Item Level Validation

    for index, item in enumerate(items, start=1):

        product_id = item.get("product_id")
        batch_number = item.get("batch_number")
        rack_id = item.get("rack_id")
        quantity = item.get("quantity")
        manufacturing_date = item.get("manufacturing_date")
        expiry_date = item.get("expiry_date")

        if not product_id:
            return f"Product is required for item {index}."

        if not batch_number:
            return f"Batch number is required for item {index}."

        if not rack_id:
            return f"Rack is required for item {index}."

        if quantity is None:
            return f"Quantity is required for item {index}."

        if quantity <= 0:
            return f"Quantity must be greater than zero for item {index}."

        if not manufacturing_date:
            return f"Manufacturing date is required for item {index}."

        if not expiry_date:
            return f"Expiry date is required for item {index}."



    # Create Shipment
    shipment = Shipment(
        received_date=received_date,
        user_id=1      # Temporary
    )

    db.session.add(shipment)

    # Get shipment_id without committing
    db.session.flush()

    # Generate shipment number
    shipment.shipment_number = f"SHP-{shipment.shipment_id:06d}"
    print(shipment.shipment_number)

    

    for item in items:
        product_id = item.get("product_id")
        batch_number = item.get("batch_number")
        rack_id = item.get("rack_id")
        quantity = item.get("quantity")
        manufacturing_date = item.get("manufacturing_date")
        expiry_date = item.get("expiry_date")




        batch = Batch.query.filter_by(
            product_id=product_id,
            batch_number=batch_number
        ).first()

        if batch is None:

            batch = Batch(
            product_id=product_id,
            batch_number=batch_number,
            manufacturing_date=manufacturing_date,
            expiry_date=expiry_date
            )

            db.session.add(batch)
            db.session.flush()


        shipment_item = ShipmentItem(
            shipment_id=shipment.shipment_id,
            product_id=product_id,
            batch_id=batch.batch_id,
            quantity=quantity
        )
        db.session.add(shipment_item)

        inventory = Inventory.query.filter_by(
            product_id=product_id,
            batch_id=batch.batch_id,
            rack_id=rack_id
        ).first()

        if inventory is None:


            inventory = Inventory(
                product_id=product_id,
                batch_id=batch.batch_id,
                rack_id=rack_id,
                quantity=0
            )

            db.session.add(inventory)
            db.session.flush()


            apply_stock_movement(
                inventory=inventory,
                quantity_change=quantity,
                movement_type="RECEIVED",
                reason="Shipment Received",
                user_id=1
            )
    

    db.session.commit()

    return shipment