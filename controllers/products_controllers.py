from flask import request, jsonify
import services.products_services as products_services


def create_product():
    data        = request.get_json()
    category_id = data.get("category_id")
    name        = data.get("name")
    sku         = data.get("sku")
    description = data.get("description")

    product = products_services.create_product(category_id, name, sku, description)

    return jsonify({
        "message": "Product created successfully",
        "data": product.to_dict()
    }), 201


def get_products():
    search      = request.args.get("search")
    category_id = request.args.get("category_id", type=int)
    page        = request.args.get("page", type=int)
    limit       = request.args.get("limit", type=int)

    products, pagination = products_services.get_products(
        search, category_id, page, limit
    )

    return jsonify({
        "message": "Products fetched successfully",
        "data": [p.to_dict() for p in products],
        "pagination": pagination
    }), 200


def get_specific_product(product_id):
    product = products_services.get_specific_product(product_id)
    return jsonify({
        "message": "Product found",
        "data": product.to_dict()
    }), 200


def update_product(product_id):
    data        = request.get_json()
    category_id = data.get("category_id")
    name        = data.get("name")
    description = data.get("description")

    product = products_services.update_product(
        product_id, category_id, name, description
    )

    return jsonify({
        "message": "Product updated successfully",
        "data": product.to_dict()
    }), 200


def delete_product(product_id):
    product = products_services.delete_product(product_id)
    return jsonify({
        "message": "Product deleted successfully",
        "data": product.to_dict()
    }), 200