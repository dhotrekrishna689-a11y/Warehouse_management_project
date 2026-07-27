from database.db_instance import db

from database.db_instance import db
from models.category import Category
from models.product import Product
from models.batch import Batch

def create_product(category_id, name, sku, description):

    # Check category exists
    category = db.session.get(Category, category_id)

    if category is None:
        return "category_not_found"

    # Check duplicate SKU
    existing_product = Product.query.filter_by(sku=sku).first()

    if existing_product:
        return "duplicate_sku"

    # Create Product
    product = Product(
        category_id=category_id,
        name=name,
        sku=sku,
        description=description
    )

    db.session.add(product)
    db.session.commit()

    return product


def get_products():

    products = Product.query.all()

    return products


def get_specific_product(product_id):

    product = db.session.get(Product, product_id)

    if product is None:
        return None

    return product

def update_product(product_id, category_id, name, description):

    product = db.session.get(Product, product_id)

    if product is None:
        return None

    category = db.session.get(Category, category_id)

    if category is None:
        return "category_not_found"

    product.category_id = category_id
    product.name = name
    product.description = description

    db.session.commit()

    return product


def delete_product(product_id):

    product = db.session.get(Product, product_id)

    if product is None:
        return None

    batch = Batch.query.filter_by(product_id=product_id).first()

    if batch:
        return "product_in_use"

    db.session.delete(product)
    db.session.commit()

    return product