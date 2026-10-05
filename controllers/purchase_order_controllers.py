from flask import request, jsonify
import services.purchase_order_services as purchase_order_services

def purchase_order():
    data = request.get_json()

    supplier_id = data.get("supplier_id")
    items = data.get("items")

    result = purchase_order_services.purchase_order(supplier_id, items)
    



    return jsonify({
        "message" : "Purchase Order Created Successfully",

    }), 201