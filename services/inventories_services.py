from models.inventory import Inventory
from models.product import Product
from models.batch import Batch
from models.rack import Rack
from database.db_instance import db
from models.stockmovement import StockMovement

def create_inventory(
    product_id,
    batch_id,
    rack_id,
    quantity
):

    # Product Exists?
    product = db.session.get(Product, product_id)

    if product is None:
        return "product_not_found"

    # Batch Exists?
    batch = db.session.get(Batch, batch_id)

    if batch is None:
        return "batch_not_found"

    # Rack Exists?
    rack = db.session.get(Rack, rack_id)

    if rack is None:
        return "rack_not_found"

    # Batch belongs to Product?
    if batch.product_id != product_id:
        return "invalid_batch_product"

    # Inventory already exists for this Batch?
    existing_inventory = Inventory.query.filter_by(
        batch_id=batch_id
    ).first()

    if existing_inventory:
        return "duplicate_inventory"

    # Quantity Validation
    if quantity < 0:
        return "invalid_quantity"

    # Create Inventory
    inventory = Inventory(
        product_id=product_id,
        batch_id=batch_id,
        rack_id=rack_id,
        quantity=quantity
    )

    db.session.add(inventory)
    db.session.commit()

    return inventory

def get_inventories():

    inventories = Inventory.query.all()

    return inventories


def get_specific_inventory(inventory_id):

    inventory = db.session.get(Inventory, inventory_id)

    if inventory is None:
        return None

    return inventory

def update_inventory(
    inventory_id,
    rack_id,
    quantity
):

    inventory = db.session.get(Inventory, inventory_id)

    if inventory is None:
        return None

    rack = db.session.get(Rack, rack_id)

    if rack is None:
        return "rack_not_found"

    if quantity < 0:
        return "invalid_quantity"

    inventory.rack_id = rack_id
    inventory.quantity = quantity

    db.session.commit()

    return inventory

def delete_inventory(inventory_id):

    inventory = db.session.get(Inventory, inventory_id)

    if inventory is None:
        return None

    stock_movement = StockMovement.query.filter_by(
        inventory_id=inventory_id
    ).first()

    if stock_movement:
        return "inventory_in_use"

    db.session.delete(inventory)
    db.session.commit()

    return inventory