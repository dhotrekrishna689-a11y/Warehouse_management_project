from database.db_instance import db
from models.shipment import Shipment
from models.product import Product
from models.batch import Batch
from models.shipmentitem import ShipmentItem


def create_shipment_item(
    shipment_id,
    product_id,
    batch_id,
    quantity
):

    shipment = db.session.get(Shipment, shipment_id)

    if shipment is None:
        return "shipment_not_found"

    product = db.session.get(Product, product_id)

    if product is None:
        return "product_not_found"

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        return "batch_not_found"

    if batch.product_id != product_id:
        return "invalid_batch"

    if quantity <= 0:
        return "invalid_quantity"

    existing_item = ShipmentItem.query.filter_by(
        shipment_id=shipment_id,
        batch_id=batch_id
    ).first()

    if existing_item:
        return "duplicate_shipment_item"

    shipment_item = ShipmentItem(
        shipment_id=shipment_id,
        product_id=product_id,
        batch_id=batch_id,
        quantity=quantity
    )

    db.session.add(shipment_item)
    db.session.commit()

    return shipment_item

def get_shipment_items():

    shipment_items = ShipmentItem.query.all()

    return shipment_items

def get_specific_shipment_item(shipment_item_id):

    shipment_item = db.session.get(
        ShipmentItem,
        shipment_item_id
    )

    if shipment_item is None:
        return None

    return shipment_item


def update_shipment_item(
    shipment_item_id,
    product_id,
    batch_id,
    quantity
):

    shipment_item = db.session.get(
        ShipmentItem,
        shipment_item_id
    )

    if shipment_item is None:
        return None

    product = db.session.get(Product, product_id)

    if product is None:
        return "product_not_found"

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        return "batch_not_found"

    if batch.product_id != product_id:
        return "invalid_batch"

    if quantity <= 0:
        return "invalid_quantity"

    existing_item = ShipmentItem.query.filter_by(
        shipment_id=shipment_item.shipment_id,
        batch_id=batch_id
    ).first()

    if existing_item:

        if existing_item.shipment_item_id != shipment_item_id:
            return "duplicate_shipment_item"

    shipment_item.product_id = product_id
    shipment_item.batch_id = batch_id
    shipment_item.quantity = quantity

    db.session.commit()

    return shipment_item


def delete_shipment_item(shipment_item_id):

    shipment_item = db.session.get(
        ShipmentItem,
        shipment_item_id
    )

    if shipment_item is None:
        return None

    db.session.delete(shipment_item)
    db.session.commit()

    return shipment_item