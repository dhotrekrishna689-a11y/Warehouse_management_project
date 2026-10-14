
from flask import Flask, request, jsonify
import services.inventories_services as inventories_services


def create_inventory():
    data = request.get_json() or {}

    product_id = data.get("product_id")
    batch_id = data.get("batch_id")
    rack_id = data.get("rack_id")
    quantity = data.get("quantity")

    inventory = inventories_services.create_inventory(
        product_id, batch_id, rack_id, quantity
    )

    return jsonify({
        "message": "Inventory created successfully",
        "data": inventory.to_dict()
    }), 201


def get_specific_inventory(inventory_id):
    inventory = inventories_services.get_specific_inventory(inventory_id)

    return jsonify({
        "message": "Inventory found",
        "data": inventory.to_dict()
    }), 200


def update_inventory(inventory_id):
    data = request.get_json() or {}

    rack_id = data.get("rack_id")
    quantity = data.get("quantity")

    inventory = inventories_services.update_inventory(
        inventory_id, rack_id, quantity
    )

    return jsonify({
        "message": "Inventory updated successfully",
        "data": inventory.to_dict()
    }), 200


def delete_inventory(inventory_id):
    inventory = inventories_services.delete_inventory(inventory_id)

    return jsonify({
        "message": "Inventory deleted successfully",
        "data": inventory.to_dict()
    }), 200


def adjust_stock(inventory_id):
    stock_data = request.get_json() or {}

    quantity = stock_data.get("quantity")
    reason = stock_data.get("reason")

    inventories_services.adjust_stock(
        inventory_id, quantity, reason
    )

    return jsonify({
        "message": "Stock adjusted successfully"
    }), 200
