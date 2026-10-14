from flask import Flask, jsonify
import controllers.purchase_order_controllers as purchase_order_controller

from flask import Blueprint

purchase_order_bp = Blueprint(
    "purchase_orders",
    __name__,
    url_prefix="/po/Purchase-order"
)


@purchase_order_bp.route("", methods = ["POST"])
def purchase_order():
    return purchase_order_controller.purchase_order()