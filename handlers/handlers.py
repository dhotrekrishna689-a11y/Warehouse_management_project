from flask import jsonify
from exceptions.exceptions import (
    # Not Found
    Resource_Not_Found_Error,
    Resource_Not_Exit_Error,
    Product_Not_Found_Error,
    Batch_Not_Found_Error,
    Rack_Not_Found_Error,
    Inventory_Not_Found_Error,
    Category_Not_Found_Error,
    Shipment_Not_Found_Error,
    Order_Not_Found_Error,
    # Duplicate
    Resource_Duplicate_Found_Error,
    Resource_existance,
    Batch_Duplicate_Found_Error,
    Category_Duplicate_Found_Error,
    Inventory_Duplicate_Found_Error,
    Rack_Duplicate_Found_Error,
    Shipment_Duplicate_Found_Error,
    Product_Duplicate_Found_Error,
    # Validation
    Validation_Error,
    Date_Validation_Error,
    Qunatity_validation_Error,
    Empty_Field_Error,
    # Cannot Delete
    Resource_Cannot_Delete,
    Category_Cannot_Delete,
    Inventory_cannot_Delete,
    Rack_Cannot_Delete,
    Shipment_Cannot_Delete,
    Product_Cannot_Delete,
    Order_Cannot_Delete,
    Order_Item_Not_Found_Error,
    Order_Item_Duplicate_Found_Error,
    Insufficient_Stock_Error,
    Shipment_Item_Not_Found_Error,
    Shipment_Item_Duplicate_Found_Error
)


def register_error_handlers(app):

    # ─── Not Found (404) ────────────────────────────────────────────────────────

    @app.errorhandler(Resource_Not_Found_Error)
    def handle_resource_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "RESOURCE_NOT_FOUND"}
        }), 404

    @app.errorhandler(Resource_Not_Exit_Error)
    def handle_resource_not_exit(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "RESOURCE_NOT_FOUND"}
        }), 404

    @app.errorhandler(Product_Not_Found_Error)
    def handle_product_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "PRODUCT_NOT_FOUND"}
        }), 404

    @app.errorhandler(Batch_Not_Found_Error)
    def handle_batch_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "BATCH_NOT_FOUND"}
        }), 404

    @app.errorhandler(Rack_Not_Found_Error)
    def handle_rack_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "RACK_NOT_FOUND"}
        }), 404

    @app.errorhandler(Inventory_Not_Found_Error)
    def handle_inventory_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "INVENTORY_NOT_FOUND"}
        }), 404

    @app.errorhandler(Category_Not_Found_Error)
    def handle_category_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "CATEGORY_NOT_FOUND"}
        }), 404

    @app.errorhandler(Shipment_Not_Found_Error)
    def handle_shipment_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "SHIPMENT_NOT_FOUND"}
        }), 404

    @app.errorhandler(Order_Not_Found_Error)
    def handle_order_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "ORDER_NOT_FOUND"}
        }), 404
    
    @app.errorhandler(Order_Item_Not_Found_Error)
    def handle_order_item_not_found(error):

        return jsonify({
        "message": str(error),
        "error": {
            "code": "ORDER_ITEM_NOT_FOUND"
        }
        }), 404

    @app.errorhandler(Shipment_Item_Not_Found_Error)
    def handle_shipment_item_not_found(error):

        return jsonify({
        "message": str(error),
        "error": {
            "code": "SHIPMENT_ITEM_NOT_FOUND"
        }
        }), 404

    

    # ─── Duplicate / Already Exists (409) ───────────────────────────────────────

    @app.errorhandler(Resource_Duplicate_Found_Error)
    def handle_duplicate(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "DUPLICATE_RESOURCE"}
        }), 409

    @app.errorhandler(Resource_existance)
    def handle_resource_existance(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "RESOURCE_ALREADY_EXISTS"}
        }), 409

    @app.errorhandler(Batch_Duplicate_Found_Error)
    def handle_batch_duplicate(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "BATCH_DUPLICATE"}
        }), 409

    @app.errorhandler(Category_Duplicate_Found_Error)
    def handle_category_duplicate(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "CATEGORY_DUPLICATE"}
        }), 409

    @app.errorhandler(Inventory_Duplicate_Found_Error)
    def handle_inventory_duplicate(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "INVENTORY_DUPLICATE"}
        }), 409

    @app.errorhandler(Rack_Duplicate_Found_Error)
    def handle_rack_duplicate(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "RACK_DUPLICATE"}
        }), 409

    @app.errorhandler(Shipment_Duplicate_Found_Error)
    def handle_shipment_duplicate(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "SHIPMENT_DUPLICATE"}
        }), 409

    @app.errorhandler(Product_Duplicate_Found_Error)
    def handle_product_duplicate(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "PRODUCT_DUPLICATE"}
        }), 409


    @app.errorhandler(Order_Item_Duplicate_Found_Error)
    def handle_order_item_duplicate(error):

        return jsonify({
        "message": str(error),
        "error": {
            "code": "ORDER_ITEM_DUPLICATE"
        }
        }), 409



    @app.errorhandler(Shipment_Item_Duplicate_Found_Error)
    def handle_shipment_item_duplicate(error):

        return jsonify({
        "message": str(error),
        "error": {
            "code": "SHIPMENT_ITEM_DUPLICATE"
        }
        }), 409

    # ─── Validation (400) ───────────────────────────────────────────────────────

    @app.errorhandler(Validation_Error)
    def handle_validation(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "VALIDATION_ERROR"}
        }), 400

    @app.errorhandler(Date_Validation_Error)
    def handle_date_validation(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "DATE_VALIDATION_ERROR"}
        }), 400

    @app.errorhandler(Qunatity_validation_Error)
    def handle_quantity_validation(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "QUANTITY_VALIDATION_ERROR"}
        }), 400

    @app.errorhandler(Empty_Field_Error)
    def handle_empty_field(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "EMPTY_FIELD_ERROR"}
        }), 400

    @app.errorhandler(Validation_Error)
    def handle_validation_error(error):

        return jsonify({
        "message": str(error),
        "error": {
            "code": "VALIDATION_ERROR"
        }
        }), 400


    # ─── Cannot Delete (409) ────────────────────────────────────────────────────

    @app.errorhandler(Resource_Cannot_Delete)
    def handle_cannot_delete(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "RESOURCE_IN_USE"}
        }), 409

    @app.errorhandler(Category_Cannot_Delete)
    def handle_category_cannot_delete(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "CATEGORY_IN_USE"}
        }), 409

    @app.errorhandler(Inventory_cannot_Delete)
    def handle_inventory_cannot_delete(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "INVENTORY_IN_USE"}
        }), 409

    @app.errorhandler(Rack_Cannot_Delete)
    def handle_rack_cannot_delete(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "RACK_IN_USE"}
        }), 409

    @app.errorhandler(Shipment_Cannot_Delete)
    def handle_shipment_cannot_delete(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "SHIPMENT_IN_USE"}
        }), 409

    @app.errorhandler(Product_Cannot_Delete)
    def handle_product_cannot_delete(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "PRODUCT_IN_USE"}
        }), 409

    @app.errorhandler(Order_Cannot_Delete)
    def handle_order_cannot_delete(error):
        return jsonify({
            "message": str(error),
            "error": {"code": "ORDER_IN_USE"}
        }), 409


    @app.errorhandler(Insufficient_Stock_Error)
    def handle_insufficient_stock(error):

        return jsonify({
        "message": str(error),
        "error": {
            "code": "INSUFFICIENT_STOCK"
        }
        }), 400