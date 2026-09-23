from flask import Flask, Request, Response



#def create_categories(name):

from models.category import Category
from models.product import Product
from database.db_instance import db
from exceptions.exceptions import (
   Resource_existance,
   Resource_Not_Exit_Error,
   Category_Not_Found_Error,
   Category_Duplicate_Found_Error,
   Category_Cannot_Delete
)


def create_categories(name):

    # Duplicate Check
    existing_category = Category.query.filter_by(name=name).first()

    if existing_category:
        #return None
        raise Resource_existance("Category already exists")

    # Create Category Object
    category = Category(
        name=name
    )

    # Save to Database
    try:
        db.session.add(category)

    # Commit
        db.session.commit()
    except Exception:
        db.session.rollback()
    # Return Created Category
    return category


def get_category():

    categories = Category.query.all()
    
    return categories


def get_specific_category(category_id):
    category = db.session.get(Category, category_id)

    if category is None:
        #return None
        raise Resource_Not_Exit_Error("Category Not exists")

    
    return category

def update_category(name, category_id):

    # Check category exists
    category = db.session.get(Category, category_id)

    if category is None:
        raise Category_Not_Found_Error("Category Not Found")

    # Check duplicate name
    get_name = Category.query.filter_by(name=name).first()

    if get_name is not None:

        if get_name.category_id != category.category_id:
            raise Category_Duplicate_Found_Error(
                "Category Already exists"
            )

    category.name = name

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return category

def delete_category(category_id):

    get_deleted_cat = db.session.get(Category, category_id)

    if get_deleted_cat is None:
        #return None
        raise Category_Not_Found_Error("Category Not Found")
    else:
        get_product = Product.query.filter_by(category_id=category_id).first()

        if get_product:
            #return "Cannot delete, beacause product already using this category"
            raise Category_Cannot_Delete("Cannot delete category because it is assigned to one or more products.")
        else:
            try:
                db.session.delete(get_deleted_cat)
                db.session.commit()
            except Exception:
                db.session.rollback()
        return get_deleted_cat