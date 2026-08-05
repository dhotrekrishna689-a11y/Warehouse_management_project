from flask import Flask, jsonify
import controllers.orders_controllers as orders_controllers

from flask import Blueprint
orders_bp = Blueprint(
    "orders",
    __name__,
    url_prefix="/orders"
)


@orders_bp.route("/", methods=["POST"])
def create_order():
    return orders_controllers.create_order()

@orders_bp.route("", methods=["GET"])
def get_orders():
    return orders_controllers.get_orders()

@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_specific_order(order_id):
    return orders_controllers.get_specific_order(order_id)

@orders_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    return orders_controllers.update_order(order_id)

@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    return orders_controllers.delete_order(order_id)


