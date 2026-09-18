from flask import request, jsonify
#from services.racks_services import racks_services
import services.racks_services as racks_services

def create_rack():

    data = request.get_json()

    rack_code = data.get("rack_code")
    capacity = data.get("capacity")

    rack = racks_services.create_rack(rack_code, capacity)

    if rack == "empty_rack_code":
        return jsonify({
            "message": "Rack code is required"
        }), 400

    if rack == "empty_capacity":
        return {
        "message": "Rack capacity is required."
        }, 400


    if rack == "duplicate_rack":
        return jsonify({
            "message": "Rack code already exists"
        }), 409

    return jsonify({
        "message": "Rack created successfully",
        "data": rack.to_dict()
    }), 201

def get_racks():

    racks = racks_services.get_racks()

    converted_racks = []

    for rack in racks:
        converted_racks.append(rack.to_dict())

    return jsonify({
        "message": "Racks fetched successfully",
        "data": converted_racks
    }), 200


def get_specific_rack(rack_id):

    rack = racks_services.get_specific_rack(rack_id)

    if rack is None:
        return jsonify({
            "message": "Rack not found"
        }), 404

    return jsonify({
        "message": "Rack found",
        "data": rack.to_dict()
    }), 200

def update_rack(rack_id):

    data = request.get_json()

    rack_code = data.get("rack_code")

    rack = racks_services.update_rack(
        rack_id,
        rack_code
    )

    if rack is None:
        return jsonify({
            "message": "Rack not found"
        }), 404

    if rack == "empty_rack_code":
        return jsonify({
            "message": "Rack code is required"
        }), 400

    if rack == "duplicate_rack":
        return jsonify({
            "message": "Rack code already exists"
        }), 409

    return jsonify({
        "message": "Rack updated successfully",
        "data": rack.to_dict()
    }), 200


def delete_rack(rack_id):

    rack = racks_services.delete_rack(rack_id)

    if rack is None:
        return jsonify({
            "message": "Rack not found"
        }), 404

    if rack == "rack_in_use":
        return jsonify({
            "message": "Cannot delete rack because inventory is using it."
        }), 409

    return jsonify({
        "message": "Rack deleted successfully",
        "data": rack.to_dict()
    }), 200


def get_rack_utilization():


    
    rack_utilization = racks_services.get_rack_utilization()

    return jsonify({
        "rack_utilization": rack_utilization
    }), 200