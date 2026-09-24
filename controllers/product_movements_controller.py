from flask import request, jsonify

from services import product_movements_services

'''
def move_product():

    movement_data = request.get_json()

    if movement_data is None:
        return jsonify({
            "message": "Invalid request body."
        }), 400

    product_movement = product_movements_services.move_product(movement_data)

    if isinstance(product_movement, str):
        return jsonify({
            "message": product_movement
        }), 400

    return jsonify({
        "message": "Product moved successfully.",
        "product_movement": product_movement.to_dict()
    }), 201
'''

from flask import request, jsonify

from services import product_movements_services


def move_product():

    movement_data = request.get_json()

    if movement_data is None:
        return jsonify({
            "message": "Invalid request body."
        }), 400

    product_movement = product_movements_services.move_product(
        movement_data
    )

    return jsonify({
        "message": "Product moved successfully.",
        "product_movement": product_movement.to_dict()
    }), 201