from flask import request, jsonify
import services.orders_services as orders_services


'''
def create_order():

    data = request.get_json()

    order_number = data.get("order_number")
    order_date = data.get("order_date")

    order = orders_services.create_order(
        order_number,
        order_date
    )

    if order == "empty_order_number":
        return jsonify({
            "message": "Order number is required"
        }), 400

    if order == "empty_order_date":
        return jsonify({
            "message": "Order date is required"
        }), 400

    if order == "duplicate_order":
        return jsonify({
            "message": "Order number already exists"
        }), 409

    return jsonify({
        "message": "Order created successfully",
        "data": order.to_dict()
    }), 201
'''

def get_orders():

    orders = orders_services.get_orders()

    converted_orders = []

    for order in orders:
        converted_orders.append(order.to_dict())

    return jsonify({
        "message": "Orders fetched successfully",
        "data": converted_orders
    }), 200


def get_specific_order(order_id):

    order = orders_services.get_specific_order(order_id)

    if order is None:
        return jsonify({
            "message": "Order not found"
        }), 404

    return jsonify({
        "message": "Order found",
        "data": order.to_dict()
    }), 200


def update_order(order_id):

    data = request.get_json()

    order_date = data.get("order_date")

    order = orders_services.update_order(
        order_id,
        order_date
    )

    if order is None:
        return jsonify({
            "message": "Order not found"
        }), 404

    if order == "empty_order_date":
        return jsonify({
            "message": "Order date is required"
        }), 400

    return jsonify({
        "message": "Order updated successfully",
        "data": order.to_dict()
    }), 200


def delete_order(order_id):

    order = orders_services.delete_order(order_id)

    if order is None:
        return jsonify({
            "message": "Order not found"
        }), 404

    if order == "order_has_items":
        return jsonify({
            "message": "Cannot delete order because it contains order items"
        }), 409

    return jsonify({
        "message": "Order deleted successfully",
        "data": order.to_dict()
    }), 200




def create_order():

    order_data = request.get_json()

    order = orders_services.create_order(order_data)

    if isinstance(order, str):
        return jsonify({
            "message": order
        }), 400

    return jsonify({
        "message": "Order created successfully.",
        "order": order.to_dict()
    }), 201


def get_pick_list(order_id):

    result = orders_services.get_pick_list(order_id)

    if isinstance(result, str):
        return jsonify({"message": result}), 404

    return jsonify(result), 200