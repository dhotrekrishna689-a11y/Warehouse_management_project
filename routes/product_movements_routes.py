from flask import Blueprint

from controllers import product_movements_controller

product_movements_bp = Blueprint(
    "product_movements",
    __name__,
    url_prefix="/product-movements"
)


@product_movements_bp.route("", methods=["POST"])
def move_product():
    return product_movements_controller.move_product()