from models.product import Product
from models.rack import Rack
from models.inventory import Inventory
from database.db_instance import db
def get_dashboard_data():

    total_products = Product.query.count()

    total_racks = Rack.query.count()

    total_stock = db.session.query(
        db.func.sum(Inventory.quantity)
    ).scalar() or 0

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "total_racks": total_racks
    }