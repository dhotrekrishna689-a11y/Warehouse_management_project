from database.db_instance import db
from models.product import Product
from models.batch import Batch
from models.inventory import Inventory
from exceptions.exceptions import (
    Product_Not_Found_Error,
    Batch_Duplicate_Found_Error,
    Date_Validation_Error,
    Resource_Not_Found_Error,
    Batch_Not_Found_Error,
    Resource_Cannot_Delete
)

def create_batch(
    product_id,
    batch_number,
    manufacturing_date,
    expiry_date
):

    # Product Exists?
    product = db.session.get(Product, product_id)

    if product is None:
        #return "product_not_found"
        raise Product_Not_Found_Error("Product not found")

    # Duplicate Batch Number?
    existing_batch = Batch.query.filter_by(
        batch_number=batch_number
    ).first()

    if existing_batch:
        #return "duplicate_batch"
        raise Batch_Duplicate_Found_Error("Duplicate Batch")

    # Date Validation
    if manufacturing_date > expiry_date:
        #return "invalid_dates"
        raise Date_Validation_Error("Invalid date")

    # Create Batch
    batch = Batch(
        product_id=product_id,
        batch_number=batch_number,
        manufacturing_date=manufacturing_date,
        expiry_date=expiry_date
    )

    try:
        db.session.add(batch)
        db.session.commit()
    except:
        db.session.rollback()
        raise

    return batch

def get_batches():

    batches = Batch.query.all()

    return batches


def get_specific_batch(batch_id):

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        #return None
        raise Batch_Not_Found_Error("Batch Not found")

    return batch

def update_batch(
    batch_id,
    product_id,
    batch_number,
    manufacturing_date,
    expiry_date
):

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        #return None
        raise Batch_Not_Found_Error("Batch Not Found")

    product = db.session.get(Product, product_id)

    if product is None:
        #return "product_not_found"
        raise Product_Not_Found_Error("Product Not Found")

    existing_batch = Batch.query.filter_by(
        batch_number=batch_number
    ).first()

    if existing_batch:

        if existing_batch.batch_id != batch.batch_id:
            #return "duplicate_batch"
            raise Batch_Duplicate_Found_Error("Duplicate Batch Found")

    if manufacturing_date > expiry_date:
        #return "invalid_dates"
        raise Date_Validation_Error("Invalid Date Found")

    batch.product_id = product_id
    batch.batch_number = batch_number
    batch.manufacturing_date = manufacturing_date
    batch.expiry_date = expiry_date

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        
    return batch





def delete_batch(batch_id):

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        #return None
        raise Batch_Not_Found_Error("Batch Not found")

    inventory = Inventory.query.filter_by(batch_id=batch_id).first()

    if inventory:
        #return "batch_in_use"
        raise Resource_Cannot_Delete("Cannot delete batch because inventory is using it.")

    try:

        db.session.delete(batch)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return batch