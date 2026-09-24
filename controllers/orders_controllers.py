from flask import request, jsonify
import services.orders_services as orders_services


def get_orders():
    orders = orders_services.get_orders()
    return jsonify({
        "message": "Orders fetched successfully",
        "data": [o.to_dict() for o in orders]
    }), 200


def get_specific_order(order_id):
    order = orders_services.get_specific_order(order_id)
    return jsonify({
        "message": "Order found",
        "data": order.to_dict()
    }), 200


def update_order(order_id):
    data       = request.get_json()
    order_date = data.get("order_date")

    order = orders_services.update_order(order_id, order_date)

    return jsonify({
        "message": "Order updated successfully",
        "data": order.to_dict()
    }), 200


def delete_order(order_id):
    order = orders_services.delete_order(order_id)
    return jsonify({
        "message": "Order deleted successfully",
        "data": order.to_dict()
    }), 200


def create_order():
    order_data = request.get_json()
    order = orders_services.create_order(order_data)
    return jsonify({
        "message": "Order created successfully.",
        "order": order.to_dict()
    }), 201


def get_pick_list(order_id):
    result = orders_services.get_pick_list(order_id)

    # Service returns a tuple (dict, status_code) for error cases
    if isinstance(result, tuple):
        data, status_code = result
        return jsonify(data), status_code

    return jsonify(result), 200


def update_inventory_after_pick(order_id):
    data  = request.get_json()
    items = data.get("items", [])

    result, status_code = orders_services.update_inventory_after_pick(
        order_id, items
    )

    return jsonify(result), status_code