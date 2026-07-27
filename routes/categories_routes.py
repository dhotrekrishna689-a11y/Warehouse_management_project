from flask import Flask, jsonify
import controllers.categories_controllers as categories_controllers

from flask import Blueprint

category_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories"
)

@category_bp.route("", methods=["POST"])
def create_catgories():
    return categories_controllers.create_catgories()



@category_bp.route("", methods=["GET"])
def get_category():
    return categories_controllers.get_category()

@category_bp.route("/<int:category_id>", methods=["GET"])
def get_specific_category(category_id):
    return categories_controllers.get_specific_category(category_id)

@category_bp.route("<int:category_id>", methods=["PUT"])
def update_category(category_id):
    return categories_controllers.update_category(category_id)

@category_bp.route("<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    return categories_controllers.delete_category(category_id)
