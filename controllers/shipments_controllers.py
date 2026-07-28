from flask import request, jsonify
import services.shipments_services as shipments_services


def create_shipment():

    data = request.get_json()

    shipment_number = data.get("shipment_number")
    received_date = data.get("received_date")
    user_id = data.get("user_id")

    shipment = shipments_services.create_shipment(
        shipment_number,
        received_date,
        user_id
    )

    if shipment == "empty_shipment_number":
        return jsonify({
            "message": "Shipment number is required"
        }), 400

    if shipment == "duplicate_shipment":
        return jsonify({
            "message": "Shipment number already exists"
        }), 409

    if shipment == "user_not_found":
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify({
        "message": "Shipment created successfully",
        "data": shipment.to_dict()
    }), 201

def get_shipments():

    shipments = shipments_services.get_shipments()

    converted_shipments = []

    for shipment in shipments:
        converted_shipments.append(shipment.to_dict())

    return jsonify({
        "message": "Shipments fetched successfully",
        "data": converted_shipments
    }), 200

def get_specific_shipment(shipment_id):

    shipment = shipments_services.get_specific_shipment(shipment_id)

    if shipment is None:
        return jsonify({
            "message": "Shipment not found"
        }), 404

    return jsonify({
        "message": "Shipment found",
        "data": shipment.to_dict()
    }), 200

def update_shipment(shipment_id):

    data = request.get_json()

    shipment_number = data.get("shipment_number")
    received_date = data.get("received_date")
    user_id = data.get("user_id")

    shipment = shipments_services.update_shipment(
        shipment_id,
        shipment_number,
        received_date,
        user_id
    )

    if shipment is None:
        return jsonify({
            "message": "Shipment not found"
        }), 404

    if shipment == "empty_shipment_number":
        return jsonify({
            "message": "Shipment number is required"
        }), 400

    if shipment == "duplicate_shipment":
        return jsonify({
            "message": "Shipment number already exists"
        }), 409

    if shipment == "user_not_found":
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify({
        "message": "Shipment updated successfully",
        "data": shipment.to_dict()
    }), 200

def delete_shipment(shipment_id):

    shipment = shipments_services.delete_shipment(shipment_id)

    if shipment is None:
        return jsonify({
            "message": "Shipment not found"
        }), 404

    if shipment == "shipment_in_use":
        return jsonify({
            "message": "Cannot delete shipment because shipment items exist."
        }), 409

    return jsonify({
        "message": "Shipment deleted successfully",
        "data": shipment.to_dict()
    }), 200