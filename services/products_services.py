from database.db_instance import db
import math
from database.db_instance import db
from models.category import Category
from models.product import Product
from models.batch import Batch
from sqlalchemy import or_

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


def get_products(search, category_id, page, limit):
    '''
    product = Product.query.all()

    return products
    '''
    if page is None:
        page = 1
    else:
        page = int(page)
    
    if limit is None:
        limit = 20
    else:
        limit = int(limit)


    query = Product.query
    search = f"%{search}%"
    if search:
        #query = query.filter_by(name=search)
        query = query.filter(
            or_(
        Product.name.ilike(search),
        Product.sku.ilike(search)
            )
        )

    if category_id:
        query = query.filter_by(category_id = category_id)

    
    total_records = query.count()

    # 5. Sorting
    query = query.order_by(Product.name.asc())

    # 6. Pagination
    offset = (page - 1) * limit

    query = query.offset(offset).limit(limit)

    # 7. Execute Query
    products = query.all()

    # 8. Total Pages
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