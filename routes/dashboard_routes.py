from flask import Blueprint
import controllers.dashboard_controller as dashboard_controller

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)

@dashboard_bp.route("", methods=["GET"])
def get_dashboard():
    return dashboard_controller.get_dashboard()