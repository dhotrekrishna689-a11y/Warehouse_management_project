from flask import Blueprint
import controllers.supplier_operation_controllers as supplier_operation_controllers


supplier_operation_bp = Blueprint(
    "supplier_operations",
    __name__,
    url_prefix="/supplier"
)


@supplier_operation_bp.route(
    "/purchase-orders/pending",
    methods=["GET"]
)
def get_pending_purchase_orders():
    return supplier_operation_controllers.get_pending_purchase_orders()


@supplier_operation_bp.route(
    "/purchase-orders/<int:purchase_order_id>",
    methods=["GET"]
)
def get_purchase_order(purchase_order_id):
    return supplier_operation_controllers.get_purchase_order(purchase_order_id)


@supplier_operation_bp.route(
    "/purchase-orders/<int:purchase_order_id>/prepare",
    methods=["POST"]
)
def prepare_purchase_order(purchase_order_id):
    return supplier_operation_controllers.prepare_purchase_order(purchase_order_id)


@supplier_operation_bp.route(
    "/purchase-orders/<int:purchase_order_id>/confirm",
    methods=["POST"]
)
def confirm_purchase_order(purchase_order_id):
    return supplier_operation_controllers.confirm_purchase_order(purchase_order_id)