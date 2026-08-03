from flask import Blueprint
import controllers.shipments_controllers as shipments_controllers
from flask import Blueprint

shipments_bp = Blueprint(
    "shipments",
    __name__,
    url_prefix="/shipments"
)

@shipments_bp.route("", methods=["POST"])
def create_shipment():
    return shipments_controllers.receive_shipment()

@shipments_bp.route("", methods=["GET"])
def get_shipments():
    return shipments_controllers.get_shipments()

@shipments_bp.route("/<int:shipment_id>", methods=["GET"])
def get_specific_shipment(shipment_id):
    return shipments_controllers.get_specific_shipment(shipment_id)

@shipments_bp.route("/<int:shipment_id>", methods=["PUT"])
def update_shipment(shipment_id):
    return shipments_controllers.update_shipment(shipment_id)

@shipments_bp.route("/<int:shipment_id>", methods=["DELETE"])
def delete_shipment(shipment_id):
    return shipments_controllers.delete_shipment(shipment_id)