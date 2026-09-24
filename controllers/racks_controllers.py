from flask import request, jsonify
import services.racks_services as racks_services


def create_rack():
    data        = request.get_json()
    rack_code   = data.get("rack_code")
    capacity    = data.get("capacity")

    rack = racks_services.create_rack(rack_code, capacity)

    return jsonify({
        "message": "Rack created successfully",
        "data": rack.to_dict()
    }), 201


def get_racks():
    racks = racks_services.get_racks()
    return jsonify({
        "message": "Racks fetched successfully",
        "data": [rack.to_dict() for rack in racks]
    }), 200


def get_specific_rack(rack_id):
    rack = racks_services.get_specific_rack(rack_id)
    return jsonify({
        "message": "Rack found",
        "data": rack.to_dict()
    }), 200


def update_rack(rack_id):
    data      = request.get_json()
    rack_code = data.get("rack_code")

    rack = racks_services.update_rack(rack_id, rack_code)

    return jsonify({
        "message": "Rack updated successfully",
        "data": rack.to_dict()
    }), 200


def delete_rack(rack_id):
    rack = racks_services.delete_rack(rack_id)
    return jsonify({
        "message": "Rack deleted successfully",
        "data": rack.to_dict()
    }), 200


def get_rack_utilization():
    rack_utilization = racks_services.get_rack_utilization()
    return jsonify({
        "rack_utilization": rack_utilization
    }), 200