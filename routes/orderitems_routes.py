from flask import Flask, jsonify
import controllers.orderitems_controllers as orderitems_controllers

from flask import Blueprint
orderitems_bp = Blueprint(
    "orderitems",
    __name__,
    url_prefix="/orderitems"
)

@orderitems_bp.route("", methods=["POST"])
def create_order_item():
    return orderitems_controllers.create_order_item()


@orderitems_bp.route("", methods=["GET"])
def get_order_items():
    return orderitems_controllers.get_order_items()

@orderitems_bp.route("/<int:order_item_id>", methods=["GET"])
def get_specific_order_item(order_item_id):
    return orderitems_controllers.get_specific_order_item(order_item_id)



@orderitems_bp.route("/<int:order_item_id>", methods=["PUT"])
def update_order_item(order_item_id):
    return orderitems_controllers.update_order_item(order_item_id)

@orderitems_bp.route("/<int:order_item_id>", methods=["DELETE"])
def delete_order_item(order_item_id):
    return orderitems_controllers.delete_order_item(order_item_id)