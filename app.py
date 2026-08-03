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
from routes.categories_routes import category_bp
from routes.products_routes import product_bp
from routes.batches_routes import batches_bp
from routes.inventories_routes import inventories_bp
from routes.racks_routes import racks_bp
from routes.shipments_routes import shipments_bp
from routes.shipmentitems_routes import shipmentitems_bp
from routes.orders_routes import orders_bp
from routes.orderitems_routes import orderitems_bp
from flask_migrate import Migrate
with app.app_context():
    db.create_all()

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

@app.route("/")
def home():
    return "Smart Warehouse Bakced Running..."

if __name__ == "__main__":
    app.run(debug=True)

