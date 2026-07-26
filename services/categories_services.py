from flask import Flask, Request, Response



#def create_categories(name):

from models.category import Category
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
    