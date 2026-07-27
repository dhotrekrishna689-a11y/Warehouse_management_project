from database.db_instance import db
from models.product import Product
from models.batch import Batch
from models.inventory import Inventory

def create_batch(
    product_id,
    batch_number,
    manufacturing_date,
    expiry_date
):

    # Product Exists?
    product = db.session.get(Product, product_id)

    if product is None:
        return "product_not_found"

    # Duplicate Batch Number?
    existing_batch = Batch.query.filter_by(
        batch_number=batch_number
    ).first()

    if existing_batch:
        return "duplicate_batch"

    # Date Validation
    if manufacturing_date > expiry_date:
        return "invalid_dates"

    # Create Batch
    batch = Batch(
        product_id=product_id,
        batch_number=batch_number,
        manufacturing_date=manufacturing_date,
        expiry_date=expiry_date
    )

    db.session.add(batch)
    db.session.commit()

    return batch

def get_batches():

    batches = Batch.query.all()

    return batches


def get_specific_batch(batch_id):

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        return None

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
        return None

    product = db.session.get(Product, product_id)

    if product is None:
        return "product_not_found"

    existing_batch = Batch.query.filter_by(
        batch_number=batch_number
    ).first()

    if existing_batch:

        if existing_batch.batch_id != batch.batch_id:
            return "duplicate_batch"

    if manufacturing_date > expiry_date:
        return "invalid_dates"

    batch.product_id = product_id
    batch.batch_number = batch_number
    batch.manufacturing_date = manufacturing_date
    batch.expiry_date = expiry_date

    db.session.commit()

    return batch





def delete_batch(batch_id):

    batch = db.session.get(Batch, batch_id)

    if batch is None:
        return None

    inventory = Inventory.query.filter_by(batch_id=batch_id).first()

    if inventory:
        return "batch_in_use"

    db.session.delete(batch)
    db.session.commit()

    return batch