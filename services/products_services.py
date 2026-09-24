from database.db_instance import db
import math
from models.category import Category
from models.product import Product
from models.batch import Batch
from sqlalchemy import or_
from exceptions.exceptions import (
    Category_Not_Found_Error,
    Product_Not_Found_Error,
    Product_Duplicate_Found_Error,
    Product_Cannot_Delete,
    Qunatity_validation_Error,
    Empty_Field_Error,
)


def create_product(category_id, name, sku, description):

    # Category exists?
    category = db.session.get(Category, category_id)
    if category is None:
        raise Category_Not_Found_Error("Category not found")

    # Duplicate SKU?
    existing_product = Product.query.filter_by(sku=sku).first()
    if existing_product:
        raise Product_Duplicate_Found_Error("A product with this SKU already exists")

    product = Product(
        category_id=category_id,
        name=name,
        sku=sku,
        description=description
    )

    try:
        db.session.add(product)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return product


def get_products(search, category_id, page, limit):

    page  = int(page)  if page  else 1
    limit = int(limit) if limit else 20

    query = Product.query

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(pattern),
                Product.sku.ilike(pattern)
            )
        )

    if category_id:
        query = query.filter_by(category_id=category_id)

    total_records = query.count()
    query = query.order_by(Product.name.asc())
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    products = query.all()
    total_pages = math.ceil(total_records / limit)

    return products, {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages
    }


def get_specific_product(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        raise Product_Not_Found_Error("Product not found")
    return product


def update_product(product_id, category_id, name, description):

    product = db.session.get(Product, product_id)
    if product is None:
        raise Product_Not_Found_Error("Product not found")

    category = db.session.get(Category, category_id)
    if category is None:
        raise Category_Not_Found_Error("Category not found")

    product.category_id = category_id
    product.name = name
    product.description = description

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return product


def delete_product(product_id):

    product = db.session.get(Product, product_id)
    if product is None:
        raise Product_Not_Found_Error("Product not found")

    batch = Batch.query.filter_by(product_id=product_id).first()
    if batch:
        raise Product_Cannot_Delete(
            "Cannot delete product because one or more batches are linked to it"
        )

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return product