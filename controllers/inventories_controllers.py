from flask import Flask, request, jsonify
import services.inventories_services as inventories_services


def create_inventory():

    # Request Receive
    data = request.get_json()

    # Data Extract
    product_id = data.get("product_id")
    batch_id = data.get("batch_id")
    rack_id = data.get("rack_id")
    quantity = data.get("quantity")

    # Service Call
    inventory = inventories_services.create_inventory(
        product_id,
        batch_id,
        rack_id,
        quantity
    )

    # Product Not Found
    if inventory == "product_not_found":
        return jsonify({
            "message": "Product not found"
        }), 404

    # Batch Not Found
    if inventory == "batch_not_found":
        return jsonify({
            "message": "Batch not found"
        }), 404

    # Rack Not Found
    if inventory == "rack_not_found":
        return jsonify({
            "message": "Rack not found"
        }), 404

    # Batch doesn't belong to Product
    if inventory == "invalid_batch_product":
        return jsonify({
            "message": "Batch does not belong to the selected product"
        }), 400

    # Inventory Already Exists
    if inventory == "duplicate_inventory":
        return jsonify({
            "message": "Inventory already exists for this batch"
        }), 409

    # Invalid Quantity
    if inventory == "invalid_quantity":
        return jsonify({
            "message": "Quantity cannot be negative"
        }), 400

    # Success
    return jsonify({
        "message": "Inventory created successfully",
        "data": inventory.to_dict()
    }), 201

def get_inventories():

    inventories = inventories_services.get_inventories()

    converted_inventories = []

    for inventory in inventories:
        converted_inventories.append(inventory.to_dict())

    return jsonify({
        "message": "Inventories fetched successfully",
        "data": converted_inventories
    }), 200


def get_specific_inventory(inventory_id):

    inventory = inventories_services.get_specific_inventory(inventory_id)

    if inventory is None:
        return jsonify({
            "message": "Inventory not found"
        }), 404

    return jsonify({
        "message": "Inventory found",
        "data": inventory.to_dict()
    }), 200


def update_inventory(inventory_id):

    data = request.get_json()

    rack_id = data.get("rack_id")
    quantity = data.get("quantity")

    inventory = inventories_services.update_inventory(
        inventory_id,
        rack_id,
        quantity
    )

    if inventory is None:
        return jsonify({
            "message": "Inventory not found"
        }), 404

    if inventory == "rack_not_found":
        return jsonify({
            "message": "Rack not found"
        }), 404

    if inventory == "invalid_quantity":
        return jsonify({
            "message": "Quantity cannot be negative"
        }), 400

    return jsonify({
        "message": "Inventory updated successfully",
        "data": inventory.to_dict()
    }), 200

def delete_inventory(inventory_id):

    inventory = inventories_services.delete_inventory(inventory_id)

    if inventory is None:
        return jsonify({
            "message": "Inventory not found"
        }), 404

    if inventory == "inventory_in_use":
        return jsonify({
            "message": "Cannot delete inventory because stock movements exist."
        }), 409

    return jsonify({
        "message": "Inventory deleted successfully",
        "data": inventory.to_dict()
    }), 200


def adjust_stock(inventory_id):

    # Request Body
    stock_data = request.get_json()

    quantity = stock_data.get("quantity")
    reason = stock_data.get("reason")

    # Service Call
    result = inventories_services.adjust_stock(
        inventory_id,
        quantity,
        reason
    )

    # Error Handling
    if result == "Inventory not found.":
        return jsonify({
            "message": result
        }), 404

    if result == "Quantity cannot be negative.":
        return jsonify({
            "message": result
        }), 400

    if result == "Reason is required.":
        return jsonify({
            "message": result
        }), 400

    if result == "No stock adjustment required.":
        return jsonify({
            "message": result
        }), 200

    # Success
    return jsonify({
        "message": "Stock adjusted successfully"
    }), 200

