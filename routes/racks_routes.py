from flask import Blueprint
import controllers.racks_controllers as racks_controllers
from flask import Blueprint

racks_bp = Blueprint(
    "racks",
    __name__,
    url_prefix="/racks"
)


@racks_bp.route("", methods=["POST"])
def create_rack():
    return racks_controllers.create_rack()

@racks_bp.route("", methods=["GET"])
def get_racks():
    return racks_controllers.get_racks()


@racks_bp.route("/<int:rack_id>", methods=["GET"])
def get_specific_rack(rack_id):
    return racks_controllers.get_specific_rack(rack_id)

@racks_bp.route("/<int:rack_id>", methods=["PUT"])
def update_rack(rack_id):
    return racks_controllers.update_rack(rack_id)

@racks_bp.route("/<int:rack_id>", methods=["DELETE"])
def delete_rack(rack_id):
    return racks_controllers.delete_rack(rack_id)


@racks_bp.route("/utilization", methods=["GET"])
def get_rack_utilization():
    return racks_controllers.get_rack_utilization()