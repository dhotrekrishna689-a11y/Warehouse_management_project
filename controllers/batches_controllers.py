from flask import Flask, request, jsonify
import services.batches_services as batches_services

def create_batch():

    # Request Receive
    data = request.get_json()

    # Data Extract
    product_id = data.get("product_id")
    batch_number = data.get("batch_number")
    manufacturing_date = data.get("manufacturing_date")
    expiry_date = data.get("expiry_date")

    # Service Call
    batch = batches_services.create_batch(
        product_id,
        batch_number,
        manufacturing_date,
        expiry_date
    )
    '''
    if batch == "product_not_found":
        return jsonify({
            "message": "Product not found"
        }), 404

    if batch == "duplicate_batch":
        return jsonify({
            "message": "Batch number already exists"
        }), 409

    if batch == "invalid_dates":
        return jsonify({
            "message": "Manufacturing date cannot be after expiry date"
        }), 400
    '''
    return jsonify({
        "message": "Batch created successfully",
        "data": batch.to_dict()
    }), 201

def get_batches():

    batches = batches_services.get_batches()

    converted_batches = []

    for batch in batches:
        converted_batches.append(batch.to_dict())

    return jsonify({
        "message": "Batches fetched successfully",
        "data": converted_batches
    }), 200

def get_specific_batch(batch_id):

    batch = batches_services.get_specific_batch(batch_id)
    '''
    if batch is None:
        return jsonify({
            "message": "Batch not found"
        }), 404
    '''
    return jsonify({
        "message": "Batch found",
        "data": batch.to_dict()
    }), 200

def update_batch(batch_id):

    data = request.get_json()

    product_id = data.get("product_id")
    batch_number = data.get("batch_number")
    manufacturing_date = data.get("manufacturing_date")
    expiry_date = data.get("expiry_date")

    batch = batches_services.update_batch(
        batch_id,
        product_id,
        batch_number,
        manufacturing_date,
        expiry_date
    )
    '''    
    if batch is None:
        return jsonify({
            "message": "Batch not found"
        }), 404

    if batch == "product_not_found":
        return jsonify({
            "message": "Product not found"
        }), 404

    if batch == "duplicate_batch":
        return jsonify({
            "message": "Batch number already exists"
        }), 409

    if batch == "invalid_dates":
        return jsonify({
            "message": "Manufacturing date cannot be after expiry date"
        }), 400
    '''
    return jsonify({
        "message": "Batch updated successfully",
        "data": batch.to_dict()
    }), 200


def delete_batch(batch_id):

    batch = batches_services.delete_batch(batch_id)

    '''
    if batch is None:
        return jsonify({
            "message": "Batch not found"
        }), 404

    if batch == "batch_in_use":
        return jsonify({
            "message": "Cannot delete batch because inventory is using it."
        }), 409
    '''
    return jsonify({
        "message": "Batch deleted successfully",
        "data": batch.to_dict()
    }), 200