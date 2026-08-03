from models.inventory import Inventory
from models.product import Product
from models.batch import Batch
from models.rack import Rack
from database.db_instance import db
from models.stockmovement import StockMovement
'''
def apply_stock_movement(inventory ,difference, movement_type = movement_type , reason=reason, user_id = user_id):
    inventory.quantity += difference
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
    
    return inventory'''

def apply_stock_movement(
    inventory,
    quantity_change,
    movement_type,
    reason,
    user_id
):

    inventory.quantity += quantity_change

    stock_movement = StockMovement(
        inventory_id=inventory.inventory_id,
        user_id=user_id,
        quantity_changed=quantity_change,
        movement_type=movement_type,
        reason=reason
    )

    db.session.add(stock_movement)

    return inventory
    