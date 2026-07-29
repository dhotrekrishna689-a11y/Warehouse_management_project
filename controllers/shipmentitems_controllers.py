from flask import request, jsonify
import services.shipmentitems_services as shipmentitems_services


def create_shipment_item():

    data = request.get_json()

    shipment_id = data.get("shipment_id")
    product_id = data.get("product_id")
    batch_id = data.get("batch_id")
    quantity = data.get("quantity")

    shipment_item = shipmentitems_services.create_shipment_item(
        shipment_id,
        product_id,
        batch_id,
        quantity
    )

    if shipment_item == "shipment_not_found":
        return jsonify({
            "message": "Shipment not found"
        }), 404

    if shipment_item == "product_not_found":
        return jsonify({
            "message": "Product not found"
        }), 404

    if shipment_item == "batch_not_found":
        return jsonify({
            "message": "Batch not found"
        }), 404

    if shipment_item == "invalid_batch":
        return jsonify({
            "message": "Batch does not belong to the selected product"
        }), 400

    if shipment_item == "invalid_quantity":
        return jsonify({
            "message": "Quantity must be greater than zero"
        }), 400

    if shipment_item == "duplicate_shipment_item":
        return jsonify({
            "message": "Shipment item already exists for this shipment and batch"
        }), 409

    return jsonify({
        "message": "Shipment item created successfully",
        "data": shipment_item.to_dict()
    }), 201

def get_shipment_items():

    shipment_items = shipmentitems_services.get_shipment_items()

    converted_items = []

    for item in shipment_items:
        converted_items.append(item.to_dict())

    return jsonify({
        "message": "Shipment items fetched successfully",
        "data": converted_items
    }), 200

def get_specific_shipment_item(shipment_item_id):

    shipment_item = shipmentitems_services.get_specific_shipment_item(
        shipment_item_id
    )

    if shipment_item is None:
        return jsonify({
            "message": "Shipment item not found"
        }), 404

    return jsonify({
        "message": "Shipment item found",
        "data": shipment_item.to_dict()
    }), 200


def update_shipment_item(shipment_item_id):

    data = request.get_json()

    product_id = data.get("product_id")
    batch_id = data.get("batch_id")
    quantity = data.get("quantity")

    shipment_item = shipmentitems_services.update_shipment_item(
        shipment_item_id,
        product_id,
        batch_id,
        quantity
    )

    if shipment_item is None:
        return jsonify({
            "message": "Shipment item not found"
        }), 404

    if shipment_item == "product_not_found":
        return jsonify({
            "message": "Product not found"
        }), 404

    if shipment_item == "batch_not_found":
        return jsonify({
            "message": "Batch not found"
        }), 404

    if shipment_item == "invalid_batch":
        return jsonify({
            "message": "Batch does not belong to the selected product"
        }), 400

    if shipment_item == "invalid_quantity":
        return jsonify({
            "message": "Quantity must be greater than zero"
        }), 400

    if shipment_item == "duplicate_shipment_item":
        return jsonify({
            "message": "Shipment item already exists for this shipment and batch"
        }), 409

    return jsonify({
        "message": "Shipment item updated successfully",
        "data": shipment_item.to_dict()
    }), 200


def delete_shipment_item(shipment_item_id):

    shipment_item = shipmentitems_services.delete_shipment_item(
        shipment_item_id
    )

    if shipment_item is None:
        return jsonify({
            "message": "Shipment item not found"
        }), 404

    return jsonify({
        "message": "Shipment item deleted successfully",
        "data": shipment_item.to_dict()
    }), 200