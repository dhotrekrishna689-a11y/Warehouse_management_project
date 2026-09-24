from database.db_instance import db
from models.shipment import Shipment
from models.product import Product
from models.batch import Batch
from models.shipmentitem import ShipmentItem

from exceptions.exceptions import (
    Shipment_Not_Found_Error,
    Product_Not_Found_Error,
    Batch_Not_Found_Error,
    Shipment_Item_Not_Found_Error,
    Shipment_Item_Duplicate_Found_Error,
    Validation_Error
)


'''
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
'''

def create_shipment_item(
    shipment_id,
    product_id,
    batch_id,
    quantity
):

    shipment = db.session.get(Shipment, shipment_id)

    if shipment is None:
        raise Shipment_Not_Found_Error(
            "Shipment Not Found"
        )

    product = db.session.get(Product, product_id)

    if product is None:
        raise Product_Not_Found_Error(
            "Product Not Found"
        )

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        raise Batch_Not_Found_Error(
            "Batch Not Found"
        )

    if batch.product_id != product_id:
        raise Validation_Error(
            "Batch does not belong to the selected product"
        )

    if quantity is None:
        raise Validation_Error(
            "Quantity is required"
        )

    if quantity <= 0:
        raise Validation_Error(
            "Quantity must be greater than zero"
        )

    existing_item = ShipmentItem.query.filter_by(
        shipment_id=shipment_id,
        batch_id=batch_id
    ).first()

    if existing_item:
        raise Shipment_Item_Duplicate_Found_Error(
            "Shipment item already exists for this shipment and batch"
        )

    shipment_item = ShipmentItem(
        shipment_id=shipment_id,
        product_id=product_id,
        batch_id=batch_id,
        quantity=quantity
    )

    try:
        db.session.add(shipment_item)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

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
        raise Shipment_Item_Not_Found_Error(
            "Shipment Item Not Found"
        )

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
        raise Shipment_Item_Not_Found_Error(
            "Shipment Item Not Found"
        )

    product = db.session.get(Product, product_id)

    if product is None:
        raise Product_Not_Found_Error(
            "Product Not Found"
        )

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        raise Batch_Not_Found_Error(
            "Batch Not Found"
        )

    if batch.product_id != product_id:
        raise Validation_Error(
            "Batch does not belong to the selected product"
        )

    if quantity is None:
        raise Validation_Error(
            "Quantity is required"
        )

    if quantity <= 0:
        raise Validation_Error(
            "Quantity must be greater than zero"
        )

    existing_item = ShipmentItem.query.filter_by(
        shipment_id=shipment_item.shipment_id,
        batch_id=batch_id
    ).first()

    if existing_item:

        if existing_item.shipment_item_id != shipment_item_id:
            raise Shipment_Item_Duplicate_Found_Error(
                "Shipment item already exists for this shipment and batch"
            )

    shipment_item.product_id = product_id
    shipment_item.batch_id = batch_id
    shipment_item.quantity = quantity

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return shipment_item


def delete_shipment_item(shipment_item_id):

    shipment_item = db.session.get(
        ShipmentItem,
        shipment_item_id
    )

    if shipment_item is None:
        raise Shipment_Item_Not_Found_Error(
            "Shipment Item Not Found"
        )

    try:
        db.session.delete(shipment_item)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return shipment_item