from flask import request, jsonify
import services.supplier_operation_services as supplier_operation_services


def get_pending_purchase_orders():

    supplier_id = request.args.get("supplier_id", type=int)

    result = supplier_operation_services.get_pending_purchase_orders(
        supplier_id
    )

    return jsonify({
        "message": "Pending Purchase Orders Fetched Successfully",
        "data": result
    }), 200


def get_purchase_order(purchase_order_id):

    result = supplier_operation_services.get_purchase_order(
        purchase_order_id
    )

    return jsonify({
        "message": "Purchase Order Fetched Successfully",
        "data": result
    }), 200


def prepare_purchase_order(purchase_order_id):

    data = request.get_json()

    result = supplier_operation_services.prepare_purchase_order(
        purchase_order_id,
        data
    )

    return jsonify({
        "message": "Purchase Order Prepared Successfully",
        "data": result
    }), 200