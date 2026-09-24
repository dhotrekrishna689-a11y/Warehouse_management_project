from flask import request, jsonify
import services.shipments_services as shipments_services


def get_shipments():
    shipments = shipments_services.get_shipments()
    return jsonify({
        "message": "Shipments fetched successfully",
        "data": [s.to_dict() for s in shipments]
    }), 200


def get_specific_shipment(shipment_id):
    shipment = shipments_services.get_specific_shipment(shipment_id)
    return jsonify({
        "message": "Shipment found",
        "data": shipment.to_dict()
    }), 200


def delete_shipment(shipment_id):
    shipment = shipments_services.delete_shipment(shipment_id)
    return jsonify({
        "message": "Shipment deleted successfully",
        "data": shipment.to_dict()
    }), 200


def receive_shipment():
    shipment_data = request.get_json()

    if shipment_data is None:
        return jsonify({"message": "Invalid request body."}), 400

    shipment = shipments_services.receive_shipment(shipment_data)

    return jsonify({
        "message": "Shipment received successfully.",
        "shipment": shipment.to_dict()
    }), 201
