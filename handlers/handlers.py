from flask import jsonify

from exceptions.exceptions import (
    Resource_Not_Found_Error,
    Resource_Duplicate_Found_Error,
    Validation_Error,
    Product_Not_Found_Error,
    Batch_Duplicate_Found_Error,
    Date_Validation_Error,
    Batch_Not_Found_Error,
    Resource_Cannot_Delete,
    Resource_existance,
    Resource_Not_Exit_Error,
    Category_Not_Found_Error,
    Category_Duplicate_Found_Error,
    Category_Cannot_Delete
)

def register_error_handlers(app):

    @app.errorhandler(Product_Not_Found_Error)
    def handle_resource_not_found(error):
        return jsonify({
            "message": str(error),
            "error": {
                "code": "PRODUCT_NOT_FOUND"
            }
        }), 404

    @app.errorhandler(Batch_Duplicate_Found_Error)
    def handle_duplicate_resource(error):
        return jsonify({
            "message": str(error),
            "error": {
                "code": "BATCH_DUPLICATE_Found"
            }
        }), 409

    @app.errorhandler(Date_Validation_Error)
    def handle_validation_error(error):
        return jsonify({
            "message": str(error),
            "error": {
                "code": "DATE_VALIDATION_ERROR"
            }
        }), 400

    @app.errorhandler(Batch_Not_Found_Error)
    def handle_validation_error(error):
        return jsonify({
            "message" : str(error),
            "error" : {
                "code" : "Batch Not found"
            }
        }), 404
    @app.errorhandler(Resource_Cannot_Delete)
    def handle_validation_error(error):
        return jsonify({
            "message": str(error),
            "error" : {
                "code" : "Batch cannot be delete"
            }
        }), 404

    @app.errorhandler(Resource_existance)
    def handle_validation_error(error):
        return jsonify({
            "message": str(error),
            "error" : {
                "code" : "Resource Exists"
            }
        }), 409

    @app.errorhandler(Resource_Not_Exit_Error)
    def handler_validation_error(error):
        return jsonify({
            "message" : str(error),
            "error" :{
                "code" : "Resource Not exits"
            }
       }),404

    @app.errorhandler(Category_Not_Found_Error)
    def handle_validation_error(error):
            return jsonify({
                "message" : str(error),
                "error" : {
                    "code" : "Category Not found"
                }
            }), 404

    @app.errorhandler(Category_Duplicate_Found_Error)
    def handle_validation_error(error):
                return jsonify({
                    "message" : str(error),
                    "error" : {
                        "code" : "Category Exits"
                    }
                }), 404
    @app.errorhandler(Category_Cannot_Delete)
    def handle_validation_error(error):
         return jsonify({
              "message":str(error),
              "error":{
                   "code": "Category cannot delete"
              }
         }),409