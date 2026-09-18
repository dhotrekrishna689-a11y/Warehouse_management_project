from flask import jsonify
import services.dashboard_service as dashboard_service


def get_dashboard():
    data = dashboard_service.get_dashboard_data()
    return jsonify(data), 200
