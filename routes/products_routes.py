from flask import Flask, jsonify
import controllers.products_controllers as products_controllers

from flask import Blueprint

product_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)

@product_bp.route("", methods=["POST"])
def create_product():
    return products_controllers.create_product()

@product_bp.route("", methods=["GET"])
def get_products():
    return products_controllers.get_products()

@product_bp.route("/<int:product_id>", methods=["GET"])
def get_specific_product(product_id):
    return products_controllers.get_specific_product(product_id)

@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    return products_controllers.update_product(product_id)

@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    return products_controllers.delete_product(product_id)