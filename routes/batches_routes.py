from flask import Flask, jsonify
import controllers.batches_controllers as batches_contollers

from flask import Blueprint

batches_bp = Blueprint(
    "batches",
    __name__,
    url_prefix="/batches"
)

@batches_bp.route("", methods=["POST"])
def create_batch_route():
    return batches_contollers.create_batch()

@batches_bp.route("", methods=["GET"])
def get_batches():
    return batches_contollers.get_batches()

@batches_bp.route("/<int:batch_id>", methods=["GET"])
def get_specific_batch(batch_id):
    return batches_contollers.get_specific_batch(batch_id)

@batches_bp.route("/<int:batch_id>", methods=["PUT"])
def update_batch(batch_id):
    return batches_contollers.update_batch(batch_id)

@batches_bp.route("/<int:batch_id>", methods=["DELETE"])
def delete_batch(batch_id):
    return batches_contollers.delete_batch(batch_id)
