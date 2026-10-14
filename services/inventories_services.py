from models.inventory import Inventory
from models.product import Product
from models.batch import Batch
from models.rack import Rack
from database.db_instance import db
from models.stockmovement import StockMovement
from models.shipment import Shipment
from services.inventory_operations import apply_stock_movement
from models.shipmentitem import ShipmentItem
from exceptions.exceptions import(
    Product_Not_Found_Error,
    Batch_Not_Found_Error,
    Rack_Not_Found_Error,
    Inventory_Duplicate_Found_Error,
    Qunatity_validation_Error,
    Validation_Error,
     Inventory_Not_Found_Error,
     Inventory_cannot_Delete
)

def create_inventory(
    product_id,
    batch_id,
    rack_id,
    quantity
):

    # Product Exists?
    product = db.session.get(Product, product_id)

    if product is None:
        #return "product_not_found"
        raise Product_Not_Found_Error("Product Not found")

    # Batch Exists?
    batch = db.session.get(Batch, batch_id)

    if batch is None:
        #return "batch_not_found"
        raise Batch_Not_Found_Error("Batch Not Found")

    # Rack Exists?
    rack = db.session.get(Rack, rack_id)

    if rack is None:
        #return "rack_not_found"
        raise Rack_Not_Found_Error("Rack Not found")
    
    # Batch belongs to Product?
    if batch.product_id != product_id:
        #return "invalid_batch_product"
        raise Validation_Error("Batch does not belong to the given product")
    # Inventory already exists for this Batch?
    existing_inventory = Inventory.query.filter_by(
        batch_id=batch_id
    ).first()

    if existing_inventory:
        #return "duplicate_inventory"
        raise Inventory_Duplicate_Found_Error("Duplicate Inventory")


    # Quantity Validation
    if quantity < 0:
        #return "invalid_quantity"
        raise Qunatity_validation_Error("Invalid Quantity canoot be negative")

    # Create Inventory
    inventory = Inventory(
        product_id=product_id,
        batch_id=batch_id,
        rack_id=rack_id,
        quantity=quantity
    )
    try:
        db.session.add(inventory)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return inventory

def get_inventories():

    inventories = Inventory.query.all()

    return inventories


def get_specific_inventory(inventory_id):

    inventory = db.session.get(Inventory, inventory_id)

    if inventory is None:
        #return None
        raise  Inventory_Not_Found_Error("Inventory Not Found")

    return inventory

def update_inventory(
    inventory_id,
    rack_id,
    quantity
):

    inventory = db.session.get(Inventory, inventory_id)

    if inventory is None:
        #return None
        raise Inventory_Not_Found_Error("Inventory Not Found")

    rack = db.session.get(Rack, rack_id)

    if rack is None:
        #return "rack_not_found"
        raise Rack_Not_Found_Error("Rack Not Found")

    if quantity < 0:
        #return "invalid_quantity"
        raise Qunatity_validation_Error("Quantity cannot be negative")

    inventory.rack_id = rack_id
    inventory.quantity = quantity
    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

    return inventory

def delete_inventory(inventory_id):

    inventory = db.session.get(Inventory, inventory_id)

    if inventory is None:
        #return None
        raise Inventory_Not_Found_Error("Inventory Not Found")

    stock_movement = StockMovement.query.filter_by(
        inventory_id=inventory_id
    ).first()

    if stock_movement:
        #return "inventory_in_use"
        raise Inventory_cannot_Delete("Cannot delete inventory because stock movements exist.")

    db.session.delete(inventory)
    db.session.commit()

    return inventory
'''
def adjust_stock(inventory_id, quantity, reason):

    # 1. Fetch Inventory
    inventory = Inventory.query.get(inventory_id)

    if inventory is None:
        return "Inventory not found."

    # 2. Validation
    if quantity < 0:
        return "Quantity cannot be negative."

    if not reason:
        return "Reason is required."

    # 3. Current Quantity
    current_quantity = inventory.quantity

    # 4. No Adjustment Required
    if current_quantity == quantity:
        return "No stock adjustment required."

    # 5. Calculate Difference
    difference = quantity - current_quantity

    updated_stockmovement_inventory = apply_stock_movement(inventory, difference, "ADJUSTEMENT", reason,user_id= 1)
    
    # 6. Update Inventory
    inventory.quantity = quantity

    # 7. Create Stock Movement
    
    stock_movement = StockMovement(
            inventory_id=inventory.inventory_id,
            user_id=1,                      # Temporary
            quantity_changed=difference,
            movement_type="ADJUSTMENT",
            reason=reason
    )
    db.session.add(stock_movement)

    # 8. Commit
    db.session.commit()

    return inventory
    '''

def adjust_stock(inventory_id, quantity, reason):

    # 1. Fetch Inventory
    inventory = Inventory.query.get(inventory_id)

    if inventory is None:
        #return "Inventory not found."
        raise Inventory_Not_Found_Error("Inventory Not Found")

    # 2. Validation
    if quantity < 0:
        #return "Quantity cannot be negative."
        raise Qunatity_validation_Error("Cannot be Negative")


    if not reason:
        #return "Reason is required."
        raise Validation_Error("Reason Is Required")

    # 3. Current Quantity
    current_quantity = inventory.quantity

    # 4. No Adjustment Required
    if current_quantity == quantity:
        #return "No stock adjustment required."
        raise Validation_Error("No stock adjustment required.")


    # 5. Calculate Difference
    quantity_change = quantity - current_quantity

    # 6. Update Inventory + Create Stock Movement
    apply_stock_movement(
        inventory=inventory,
        quantity_change=quantity_change,
        movement_type="ADJUSTMENT",
        reason=reason,
        user_id=1      # Temporary
    )

    # 7. Commit
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

    return inventory



