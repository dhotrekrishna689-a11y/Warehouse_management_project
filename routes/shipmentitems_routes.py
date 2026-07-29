from flask import Blueprint
import controllers.shipmentitems_controllers as shipmentitems_controllers
from flask import Blueprint

shipmentitems_bp = Blueprint(
    "shipmentitems",
    __name__,
    url_prefix="/shipmentitems"
)

@shipmentitems_bp.route("", methods=["POST"])
def create_shipment_item():
    return shipmentitems_controllers.create_shipment_item()

@shipmentitems_bp.route("", methods=["GET"])
def get_shipment_items():
    return shipmentitems_controllers.get_shipment_items()

@shipmentitems_bp.route("/<int:shipment_item_id>", methods=["GET"])
def get_specific_shipment_item(shipment_item_id):
    return shipmentitems_controllers.get_specific_shipment_item(shipment_item_id)

@shipmentitems_bp.route("/<int:shipment_item_id>", methods=["PUT"])
def update_shipment_item(shipment_item_id):
    return shipmentitems_controllers.update_shipment_item(
        shipment_item_id
    )


@shipmentitems_bp.route("/<int:shipment_item_id>", methods=["DELETE"])
def delete_shipment_item(shipment_item_id):
    return shipmentitems_controllers.delete_shipment_item(
        shipment_item_id
    )