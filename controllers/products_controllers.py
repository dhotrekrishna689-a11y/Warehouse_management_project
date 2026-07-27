from flask import Flask, request, jsonify
import services.products_services as products_services
from models.batch import Batch


def create_product():

    # Request receive
    data = request.get_json()

    # Data extract
    category_id = data.get("category_id")
    name = data.get("name")
    sku = data.get("sku")
    description = data.get("description")

    # Service call
    product = products_services.create_product(
        category_id,
        name,
        sku,
        description
    )

    # Category not found
    if product == "category_not_found":
        return jsonify({
            "message": "Category not found"
        }), 404

    # Duplicate SKU
    if product == "duplicate_sku":
        return jsonify({
            "message": "SKU already exists"
        }), 409

    # Success
    return jsonify({
        "message": "Product created successfully",
        "data": product.to_dict()
    }), 201


def get_products():

    # Service Call
    products = products_services.get_products()

    # Convert Objects to Dictionary
    converted_products = []

    for product in products:
        converted_products.append(product.to_dict())

    # Response
    return jsonify({
        "message": "Products fetched successfully",
        "data": converted_products
    }), 200


def get_specific_product(product_id):

    # Service Call
    product = products_services.get_specific_product(product_id)

    # Product not found
    if product is None:
        return jsonify({
            "message": "Product not found"
        }), 404

    # Success
    return jsonify({
        "message": "Product found",
        "data": product.to_dict()
    }), 200

def update_product(product_id):

    data = request.get_json()

    category_id = data.get("category_id")
    name = data.get("name")
    description = data.get("description")

    update_product = products_services.update_product(
        product_id,
        category_id,
        name,
        description
    )

    if update_product is None:
        return jsonify({
            "message": "Product not found"
        }), 404

    if update_product == "category_not_found":
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify({
        "message": "Product updated successfully",
        "data": update_product.to_dict()
    }), 200

def delete_product(product_id):

    delete_product = products_services.delete_product(product_id)

    if delete_product is None:
        return jsonify({
            "message": "Product not found"
        }), 404

    if delete_product == "product_in_use":
        return jsonify({
            "message": "Cannot delete product because it is being used."
        }), 409

    return jsonify({
        "message": "Product deleted successfully",
        "data": delete_product.to_dict()
    }), 200