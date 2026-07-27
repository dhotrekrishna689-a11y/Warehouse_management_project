from flask import Flask, Request, Response



#def create_categories(name):

from models.category import Category
from models.product import Product
from database.db_instance import db


def create_categories(name):

    # Duplicate Check
    existing_category = Category.query.filter_by(name=name).first()

    if existing_category:
        return None

    # Create Category Object
    category = Category(
        name=name
    )

    # Save to Database
    db.session.add(category)

    # Commit
    db.session.commit()

    # Return Created Category
    return category


def get_category():

    categories = Category.query.all()
    
    return categories


def get_specific_category(category_id):
    category = db.session.get(Category, category_id)

    if category is None:
        return None

    
    return category

def update_category(name, category_id):

    # Check category exists
    category = db.session.get(Category, category_id)

    if category is None:
        return None

    # Check duplicate name
    get_name = Category.query.filter_by(name=name).first()

    if get_name is None:

        category.name = name
        db.session.commit()
        return category

    else:

        if get_name.category_id == category.category_id:

            category.name = name
            db.session.commit()
            return category

        else:
            return "duplicate"

def delete_category(category_id):

    get_deleted_cat = db.session.get(Category, category_id)

    if get_deleted_cat is None:
        return None
    else:
        get_product = Product.query.filter_by(category_id=category_id).first()

        if get_product:
            return "Cannot delete, beacause product already using this category"
        else:
            db.session.delete(get_deleted_cat)
            db.session.commit()
            return get_deleted_cat