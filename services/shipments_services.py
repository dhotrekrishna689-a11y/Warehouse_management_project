from database.db_instance import db
from models.shipment import Shipment
from models.shipmentitem import ShipmentItem
from models.inventory import Inventory
from models.batch import Batch
from models.rack import Rack
from models.product import Product
from services.inventory_operations import apply_stock_movement
from exceptions.exceptions import (
    Shipment_Not_Found_Error,
    Shipment_Duplicate_Found_Error,
    Shipment_Cannot_Delete,
    Product_Not_Found_Error,
    Rack_Not_Found_Error,
    Validation_Error,
    Qunatity_validation_Error,
    Empty_Field_Error,
)


def get_shipments():
    return Shipment.query.all()


def get_specific_shipment(shipment_id):
    shipment = db.session.get(Shipment, shipment_id)
    if shipment is None:
        raise Shipment_Not_Found_Error("Shipment not found")
    return shipment


def delete_shipment(shipment_id):

    shipment = db.session.get(Shipment, shipment_id)
    if shipment is None:
        raise Shipment_Not_Found_Error("Shipment not found")

    shipment_item = ShipmentItem.query.filter_by(shipment_id=shipment_id).first()
    if shipment_item:
        raise Shipment_Cannot_Delete(
            "Cannot delete shipment because it has shipment items linked to it"
        )

    try:
        db.session.delete(shipment)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return shipment


def receive_shipment(shipment_data):

    # ── Shipment-level validation ────────────────────────────────────────────────
    received_date = shipment_data.get("received_date")
    items         = shipment_data.get("items")

    if not received_date:
        raise Empty_Field_Error("Received date is required")

    if not items:
        raise Validation_Error("Shipment must contain at least one item")

    # ── Item-level validation ────────────────────────────────────────────────────
    for index, item in enumerate(items, start=1):
        product_id        = item.get("product_id")
        batch_number      = item.get("batch_number")
        rack_id           = item.get("rack_id")
        quantity          = item.get("quantity")
        manufacturing_date = item.get("manufacturing_date")
        expiry_date       = item.get("expiry_date")

        if not product_id:
            raise Empty_Field_Error(f"Product is required for item {index}")
        if not batch_number:
            raise Empty_Field_Error(f"Batch number is required for item {index}")
        if not rack_id:
            raise Empty_Field_Error(f"Rack is required for item {index}")
        if quantity is None:
            raise Empty_Field_Error(f"Quantity is required for item {index}")
        if quantity <= 0:
            raise Qunatity_validation_Error(
                f"Quantity must be greater than zero for item {index}"
            )
        if not manufacturing_date:
            raise Empty_Field_Error(f"Manufacturing date is required for item {index}")
        if not expiry_date:
            raise Empty_Field_Error(f"Expiry date is required for item {index}")

        # FK checks
        if not db.session.get(Product, product_id):
            raise Product_Not_Found_Error(
                f"Product ID {product_id} not found for item {index}"
            )
        if not db.session.get(Rack, rack_id):
            raise Rack_Not_Found_Error(
                f"Rack ID {rack_id} not found for item {index}"
            )

    # ── Create Shipment ──────────────────────────────────────────────────────────
    shipment = Shipment(received_date=received_date, user_id=1)
    db.session.add(shipment)
    db.session.flush()
    shipment.shipment_number = f"SHP-{shipment.shipment_id:06d}"

    for item in items:
        product_id         = item.get("product_id")
        batch_number       = item.get("batch_number")
        rack_id            = item.get("rack_id")
        quantity           = item.get("quantity")
        manufacturing_date = item.get("manufacturing_date")
        expiry_date        = item.get("expiry_date")

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

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return shipment