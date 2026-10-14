'''
from dotenv import load_dotenv
from flask import Flask
from database.db_instance import db
import os


load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

from models.category import Category
from models.product import Product
from models.batch import Batch
from models.rack import Rack
from models.inventory import Inventory
from models.user import User
from models.shipment import Shipment
from models.shipmentitem import ShipmentItem
from models.order import Order
from models.orderitem import OrderItem
from models.stockmovement import StockMovement
from models.purchase_order import Purchase_Order
from models.purchase_order_item import Purchase_Order_Item
from models.supplier import Supplier
from models.supplier_order_preparation import Supplier_Order_Preparation
from models.supplier_order_preparation_item import Supplier_Order_Preparation_Item
from routes.categories_routes import category_bp
from routes.products_routes import product_bp
from routes.batches_routes import batches_bp
from routes.inventories_routes import inventories_bp
from routes.racks_routes import racks_bp
from routes.shipments_routes import shipments_bp
from routes.shipmentitems_routes import shipmentitems_bp
from routes.orders_routes import orders_bp
from routes.orderitems_routes import orderitems_bp
from routes.purchase_order_routes import purchase_order_bp 
from flask_migrate import Migrate
from models.productmovement import ProductMovement
from routes.product_movements_routes import product_movements_bp
<<<<<<< HEAD
from routes.dashboard_routes import dashboard_bp
with app.app_context():
    db.create_all()
    try:
        db.session.execute(db.text("ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'PENDING';"))
        db.session.commit()
    except Exception:
        db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE orders ADD COLUMN status VARCHAR(50) DEFAULT 'PENDING';"))
            db.session.commit()
        except Exception:
            db.session.rollback()
=======
from routes.supplier_operation_routes import supplier_operation_bp
#from routes.dashboard_routes import dashboard_bp
from handlers.handlers import register_error_handlers
>>>>>>> backend

#with app.app_context():
 #   db.create_all()

register_error_handlers(app)
migrate = Migrate(app, db)

app.register_blueprint(category_bp)
app.register_blueprint(product_bp)
app.register_blueprint(batches_bp)
app.register_blueprint(inventories_bp)
app.register_blueprint(racks_bp)
app.register_blueprint(shipments_bp)
app.register_blueprint(shipmentitems_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(orderitems_bp)
app.register_blueprint(product_movements_bp)
<<<<<<< HEAD
app.register_blueprint(dashboard_bp)
=======
#app.register_blueprint(dashboard_bp)
app.register_blueprint(purchase_order_bp )
app.register_blueprint(supplier_operation_bp)
>>>>>>> backend

@app.route("/")
def home():
    return "Smart Warehouse Bakced Running..."

if __name__ == "__main__":
    app.run(debug=True)'''

from dotenv import load_dotenv
from flask import Flask
from database.db_instance import db
from flask_migrate import Migrate
from handlers.handlers import register_error_handlers
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db.init_app(app)

# Models
from models.category import Category
from models.product import Product
from models.batch import Batch
from models.rack import Rack
from models.inventory import Inventory
from models.user import User
from models.shipment import Shipment
from models.shipmentitem import ShipmentItem
from models.order import Order
from models.orderitem import OrderItem
from models.stockmovement import StockMovement
from models.productmovement import ProductMovement
from models.purchase_order import Purchase_Order
from models.purchase_order_item import Purchase_Order_Item
from models.supplier import Supplier
from models.supplier_order_preparation import Supplier_Order_Preparation
from models.supplier_order_preparation_item import Supplier_Order_Preparation_Item

# Routes
from routes.categories_routes import category_bp
from routes.products_routes import product_bp
from routes.batches_routes import batches_bp
from routes.inventories_routes import inventories_bp
from routes.racks_routes import racks_bp
from routes.shipments_routes import shipments_bp
from routes.shipmentitems_routes import shipmentitems_bp
from routes.orders_routes import orders_bp
from routes.orderitems_routes import orderitems_bp
from routes.product_movements_routes import product_movements_bp
from routes.purchase_order_routes import purchase_order_bp
from routes.supplier_operation_routes import supplier_operation_bp
from routes.dashboard_routes import dashboard_bp

# Error handling and migrations
register_error_handlers(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(category_bp)
app.register_blueprint(product_bp)
app.register_blueprint(batches_bp)
app.register_blueprint(inventories_bp)
app.register_blueprint(racks_bp)
app.register_blueprint(shipments_bp)
app.register_blueprint(shipmentitems_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(orderitems_bp)
app.register_blueprint(product_movements_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(purchase_order_bp)
app.register_blueprint(supplier_operation_bp)


@app.route("/")
def home():
    return "Smart Warehouse Backend Running..."


if __name__ == "__main__":
    app.run(debug=True)


