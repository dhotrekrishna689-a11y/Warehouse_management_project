from flask import request, jsonify
import services.orderitems_services as orderitems_services

'''
def create_order_item():

    data = request.get_json()

    order_id = data.get("order_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    order_item = orderitems_services.create_order_item(
        order_id,
        product_id,
        quantity
    )
    
    if order_item == "empty_order_id":
        return jsonify({
            "message": "Order ID is required"
        }), 400

    if order_item == "empty_product_id":
        return jsonify({
            "message": "Product ID is required"
        }), 400

    if order_item == "empty_quantity":
        return jsonify({
            "message": "Quantity is required"
        }), 400

    if order_item == "order_not_found":
        return jsonify({
            "message": "Order not found"
        }), 404

    if order_item == "product_not_found":
        return jsonify({
            "message": "Product not found"
        }), 404

    if order_item == "duplicate_order_item":
        return jsonify({
            "message": "Order item already exists for this order"
        }), 409
    


    return jsonify({
        "message": "Order item created successfully",
        "data": order_item.to_dict()
    }), 201

def get_order_items():

    order_items = orderitems_services.get_order_items()

    converted_order_items = []

    for order_item in order_items:
        converted_order_items.append(order_item.to_dict())

    return jsonify({
        "message": "Order items fetched successfully",
        "data": converted_order_items
    }), 200

def get_specific_order_item(order_item_id):

    order_item = orderitems_services.get_specific_order_item(
        order_item_id
    )

    if order_item is None:
        return jsonify({
            "message": "Order item not found"
        }), 404

    return jsonify({
        "message": "Order item found",
        "data": order_item.to_dict()
    }), 200

def update_order_item(order_item_id):

    data = request.get_json()

    quantity = data.get("quantity")

    order_item = orderitems_services.update_order_item(
        order_item_id,
        quantity
    )

    if order_item is None:
        return jsonify({
            "message": "Order item not found"
        }), 404

    if order_item == "empty_quantity":
        return jsonify({
            "message": "Quantity is required"
        }), 400

    if order_item == "invalid_quantity":
        return jsonify({
            "message": "Quantity must be greater than zero"
        }), 400

    return jsonify({
        "message": "Order item updated successfully",
        "data": order_item.to_dict()
    }), 200

def delete_order_item(order_item_id):

    order_item = orderitems_services.delete_order_item(
        order_item_id
    )

    if order_item is None:
        return jsonify({
            "message": "Order item not found"
        }), 404

    return jsonify({
        "message": "Order item deleted successfully",
        "data": order_item.to_dict()
    }), 200'''

def create_order_item():

    data = request.get_json()

    order_id = data.get("order_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    order_item = orderitems_services.create_order_item(
        order_id,
        product_id,
        quantity
    )

    return jsonify({
        "message": "Order item created successfully",
        "data": order_item.to_dict()
    }), 201


def get_order_items():

    order_items = orderitems_services.get_order_items()

    converted_order_items = []

    for order_item in order_items:
        converted_order_items.append(
            order_item.to_dict()
        )

    return jsonify({
        "message": "Order items fetched successfully",
        "data": converted_order_items
    }), 200


def get_specific_order_item(order_item_id):

    order_item = orderitems_services.get_specific_order_item(
        order_item_id
    )

    return jsonify({
        "message": "Order item found",
        "data": order_item.to_dict()
    }), 200


def update_order_item(order_item_id):

    data = request.get_json()

    quantity = data.get("quantity")

    order_item = orderitems_services.update_order_item(
        order_item_id,
        quantity
    )

    return jsonify({
        "message": "Order item updated successfully",
        "data": order_item.to_dict()
    }), 200


def delete_order_item(order_item_id):

    order_item = orderitems_services.delete_order_item(
        order_item_id
    )

    return jsonify({
        "message": "Order item deleted successfully",
        "data": order_item.to_dict()
    }), 200