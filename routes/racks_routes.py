from flask import Blueprint
import controllers.racks_controllers as racks_controllers

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


# ⚠️ /utilization MUST be above /<int:rack_id> — otherwise Flask will try
# to parse "utilization" as an integer and return 404.
@racks_bp.route("/utilization", methods=["GET"])
def get_rack_utilization():
    return racks_controllers.get_rack_utilization()


@racks_bp.route("/<int:rack_id>", methods=["GET"])
def get_specific_rack(rack_id):
    return racks_controllers.get_specific_rack(rack_id)


@racks_bp.route("/<int:rack_id>", methods=["PUT"])
def update_rack(rack_id):
    return racks_controllers.update_rack(rack_id)


@racks_bp.route("/<int:rack_id>", methods=["DELETE"])
def delete_rack(rack_id):
    return racks_controllers.delete_rack(rack_id)