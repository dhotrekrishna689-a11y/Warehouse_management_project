from dotenv import load_dotenv
from flask import Flask
from database.db_instance import db
import os

load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

@app.route("/")
def home():
    return "Smart Warehouse Bakced Running..."

if __name__ == "__main__":
    app.run(debug=True)

