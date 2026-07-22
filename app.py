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

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Smart Warehouse Bakced Running..."

if __name__ == "__main__":
    app.run(debug=True)

