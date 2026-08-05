from models.inventory import Inventory
from models.productmovement import ProductMovement
from services.inventories_services import apply_stock_movement
from database.db_instance import db


def move_product(movement_data):

    # -----------------------------
    # 1. Validation
    # -----------------------------

    product_id = movement_data.get("product_id")
    batch_id = movement_data.get("batch_id")
    source_rack_id = movement_data.get("source_rack_id")
    destination_rack_id = movement_data.get("destination_rack_id")
    quantity = movement_data.get("quantity")
    reason = movement_data.get("reason")

    if not product_id:
        return "Product is required."

    if not batch_id:
        return "Batch is required."

    if not source_rack_id:
        return "Source rack is required."

    if not destination_rack_id:
        return "Destination rack is required."

    if source_rack_id == destination_rack_id:
        return "Source and destination rack cannot be the same."

    if quantity is None:
        return "Quantity is required."

    if quantity <= 0:
        return "Quantity must be greater than zero."

    if not reason:
        return "Reason is required."

    # -----------------------------
    # 2. Find Source Inventory
    # -----------------------------

    source_inventory = Inventory.query.filter_by(
        product_id=product_id,
        batch_id=batch_id,
        rack_id=source_rack_id
    ).first()

    if source_inventory is None:
        return "Source inventory not found."

    if source_inventory.quantity < quantity:
        return "Insufficient stock in source rack."

    # -----------------------------
    # 3. Find/Create Destination Inventory
    # -----------------------------

    destination_inventory = Inventory.query.filter_by(
        product_id=product_id,
        batch_id=batch_id,
        rack_id=destination_rack_id
    ).first()

    if destination_inventory is None:

        destination_inventory = Inventory(
            product_id=product_id,
            batch_id=batch_id,
            rack_id=destination_rack_id,
            quantity=0
        )

        db.session.add(destination_inventory)
        db.session.flush()

    # -----------------------------
    # 4. Create Product Movement
    # -----------------------------

    product_movement = ProductMovement(
        product_id=product_id,
        batch_id=batch_id,
        source_rack_id=source_rack_id,
        destination_rack_id=destination_rack_id,
        quantity=quantity,
        reason=reason,
        user_id=1
    )

    db.session.add(product_movement)

    # -----------------------------
    # 5. Move Stock
    # -----------------------------

    apply_stock_movement(
        source_inventory,
        -quantity,
        "MOVED_OUT",
        reason,
        1
    )

    apply_stock_movement(
        destination_inventory,
        quantity,
        "MOVED_IN",
        reason,
        1
    )

    db.session.commit()

    return product_movement