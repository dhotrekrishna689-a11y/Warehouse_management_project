from flask import Flask, jsonify
import controllers.inventories_controllers as inventories_controllers

from flask import Blueprint
inventories_bp = Blueprint(
    "inventories",
    __name__,
    url_prefix="/inventories"
)

@inventories_bp.route("", methods=["POST"])
def create_inventory():
    return inventories_controllers.create_inventory()

@inventories_bp.route("", methods=["GET"])
def get_inventories():
    return inventories_controllers.get_inventories()

@inventories_bp.route("/<int:inventory_id>", methods=["GET"])
def get_specific_inventory(inventory_id):
    return inventories_controllers.get_specific_inventory(inventory_id)


@inventories_bp.route("/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
    return inventories_controllers.update_inventory(inventory_id)

@inventories_bp.route("/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
    return inventories_controllers.delete_inventory(inventory_id)

@inventories_bp.route("/<int:inventory_id>", methods=["PATCH"])
def adjust_stock(inventory_id):
    return inventories_controllers.adjust_stock(inventory_id)