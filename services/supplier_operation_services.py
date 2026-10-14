from database.db_instance import db

from models.purchase_order import Purchase_Order
from models.purchase_order_item import Purchase_Order_Item

from exceptions.exceptions import(
    Purchase_Order_Not_Found,
    Required_Field,
    Qunatity_validation_Error
)

import base64
import io
import json

import qrcode

from database.db_instance import db
from models.purchase_order import Purchase_Order
from models.supplier_order_preparation import Supplier_Order_Preparation


def get_pending_purchase_orders(supplier_id):
    print("Starting a service layear logic:")
    
    purchase_orders = Purchase_Order.query.filter_by(
        supplier_id=supplier_id,
        status="Pending"
    ).all()

    print("Purchase order:", purchase_orders)
    result = []

    for purchase_order in purchase_orders:

        items = []

        for item in purchase_order.purchase_order_items:

            items.append({
                "product_id": item.product_id,
                "ordered_quantity": item.ordered_quantity
            })

        result.append({
            "purchase_order_id": purchase_order.purchase_order_id,
            "purchase_order_number": purchase_order.purchase_order_number,
            "order_date": purchase_order.order_date,
            "status": purchase_order.status,
            "items": items
        })

        

    return result


def get_purchase_order(purchase_order_id):

    purchase_order = Purchase_Order.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if purchase_order is None:
        raise Purchase_Order_Not_Found("Purchase id not exist's")

    items = []

    for item in purchase_order.purchase_order_items:

        items.append({
            "product_id": item.product_id,
            "product_name": item.product.name,
            "ordered_quantity": item.ordered_quantity
        })

    return {
        "purchase_order_id": purchase_order.purchase_order_id,
        "purchase_order_number": purchase_order.purchase_order_number,
        "supplier_id": purchase_order.supplier_id,
        "order_date": purchase_order.order_date,
        "status": purchase_order.status,
        "items": items
    }


'''
def prepare_purchase_order(purchase_order_id, data):

    purchase_order = Purchase_Order.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if purchase_order is None:
        raise Purchase_Order_Not_Found("Purchase Order not found")

    items = data.get("items")

    if items is None:
        raise Required_Field("Item is Required")

    expected_dispatch_date = data.get("expected_dispatch_date")
    expected_delivery_date = data.get("expected_delivery_date")

    for item in items:

        prepared_quantity = item.get("prepared_quantity")
        manufacturing_date = item.get("manufacturing_date")
        expiry_date = item.get("expiry_date")

        if prepared_quantity is None:
           raise Required_Field("Quantity is required")

        if prepared_quantity <= 0:
            raise Qunatity_validation_Error("Quantity must be greater than zero")
            

        if manufacturing_date is None:
            raise Required_Field("Manufacturing date is required")

    return {
        "purchase_order_id": purchase_order.purchase_order_id,
        "status": purchase_order.status,
        "items": items,
        "expected_dispatch_date": expected_dispatch_date,
        "expected_delivery_date": expected_delivery_date
    }



def confirm_purchase_order(purchase_order_id):

    purchase_order = Purchase_Order.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if purchase_order is None:
        return {
            "error": "Purchase Order not found"
        }

    if purchase_order.status != "Pending":
        return {
            "error": "Purchase Order is not in Pending status"
        }

    # Abhi yaha:
    # 1. Shipment number generate
    # 2. Batch number generate
    # 3. QR generate
    # 4. PO status Prepared
    # implement karenge

    return {
        "purchase_order_id": purchase_order.purchase_order_id,
        "purchase_order_number": purchase_order.purchase_order_number,
        "status": purchase_order.status
    }
'''





def prepare_purchase_order(purchase_order_id, data):

    purchase_order = Purchase_Order.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if purchase_order is None:
        raise Purchase_Order_Not_Found("Purchase Order not found")

    if purchase_order.status != "Pending":
        raise Required_Field(
            "Purchase Order is not in Pending status"
        )

    # Check whether preparation already exists
    existing_preparation = Supplier_Order_Preparation.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if existing_preparation is not None:
        raise Required_Field(
            "Preparation already exists for this Purchase Order"
        )

    items = data.get("items")

    if not items:
        raise Required_Field("Items are required")

    expected_dispatch_date = data.get("expected_dispatch_date")
    expected_delivery_date = data.get("expected_delivery_date")

    if not expected_dispatch_date or not expected_delivery_date:
        raise Required_Field(
            "Expected dispatch and delivery dates are required"
        )

    try:
        expected_dispatch_date = date.fromisoformat(
            expected_dispatch_date
        )
        expected_delivery_date = date.fromisoformat(
            expected_delivery_date
        )
    except (ValueError, TypeError):
        raise Required_Field("Dates must use YYYY-MM-DD format")

    if expected_delivery_date < expected_dispatch_date:
        raise Required_Field(
            "Expected delivery date cannot be before dispatch date"
        )

    # Match supplier items with the actual PO items
    po_items = {
        po_item.product_id: po_item
        for po_item in purchase_order.purchase_order_items
    }

    validated_items = []
    seen_product_ids = set()

    for item in items:

        product_id = item.get("product_id")
        prepared_quantity = item.get("prepared_quantity")
        manufacturing_date = item.get("manufacturing_date")
        expiry_date = item.get("expiry_date")

        if product_id is None or product_id not in po_items:
            raise Required_Field(
                "Product does not belong to this Purchase Order"
            )

        if product_id in seen_product_ids:
            raise Required_Field(
                "Duplicate product items are not allowed"
            )

        seen_product_ids.add(product_id)

        if prepared_quantity is None:
            raise Required_Field("Prepared quantity is required")

        if not isinstance(prepared_quantity, int) or isinstance(
            prepared_quantity, bool
        ):
            raise Qunatity_validation_Error(
                "Prepared quantity must be an integer"
            )

        if prepared_quantity <= 0:
            raise Qunatity_validation_Error(
                "Prepared quantity must be greater than zero"
            )

        if prepared_quantity > po_items[product_id].ordered_quantity:
            raise Qunatity_validation_Error(
                "Prepared quantity cannot exceed ordered quantity"
            )

        if not manufacturing_date:
            raise Required_Field("Manufacturing date is required")

        try:
            manufacturing_date = date.fromisoformat(
                manufacturing_date
            )

            if expiry_date:
                expiry_date = date.fromisoformat(expiry_date)

        except (ValueError, TypeError):
            raise Required_Field("Item dates must use YYYY-MM-DD format")

        if expiry_date and expiry_date < manufacturing_date:
            raise Required_Field(
                "Expiry date cannot be before manufacturing date"
            )

        validated_items.append({
            "product_id": product_id,
            "prepared_quantity": prepared_quantity,
            "manufacturing_date": manufacturing_date,
            "expiry_date": expiry_date
        })

    try:
        # Save header information
        preparation = Supplier_Order_Preparation(
            purchase_order_id=purchase_order.purchase_order_id,
            expected_dispatch_date=expected_dispatch_date,
            expected_delivery_date=expected_delivery_date,
            shipment_number=None,
            status="Pending"
        )

        db.session.add(preparation)
        db.session.flush()

        # Save product-wise preparation information
        for item in validated_items:

            preparation_item = Supplier_Order_Preparation_Item(
                preparation_id=preparation.preparation_id,
                product_id=item["product_id"],
                prepared_quantity=item["prepared_quantity"],
                manufacturing_date=item["manufacturing_date"],
                expiry_date=item["expiry_date"],
                batch_number=None
            )

            db.session.add(preparation_item)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "purchase_order_id": purchase_order.purchase_order_id,
        "preparation_id": preparation.preparation_id,
        "status": preparation.status,
        "expected_dispatch_date": expected_dispatch_date.isoformat(),
        "expected_delivery_date": expected_delivery_date.isoformat(),
        "items": [
            {
                "product_id": item["product_id"],
                "prepared_quantity": item["prepared_quantity"],
                "manufacturing_date": item[
                    "manufacturing_date"
                ].isoformat(),
                "expiry_date": (
                    item["expiry_date"].isoformat()
                    if item["expiry_date"] else None
                )
            }
            for item in validated_items
        ]
    }


def confirm_purchase_order(purchase_order_id):

    purchase_order = Purchase_Order.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if purchase_order is None:
        raise Purchase_Order_Not_Found("Purchase Order not found")

    if purchase_order.status != "Pending":
        raise Required_Field(
            "Purchase Order is not in Pending status"
        )

    preparation = Supplier_Order_Preparation.query.filter_by(
        purchase_order_id=purchase_order_id
    ).first()

    if preparation is None:
        raise Required_Field(
            "Prepare the Purchase Order before confirmation"
        )

    if preparation.status != "Pending":
        raise Required_Field(
            "Preparation has already been confirmed or processed"
        )

    if not preparation.preparation_items:
        raise Required_Field("Preparation items not found")

    try:
        # Generate identifiers only at confirmation
        preparation.shipment_number = (
            f"SHP-{preparation.preparation_id:06d}"
        )

        for item in preparation.preparation_items:
            item.batch_number = (
                f"BATCH-{item.preparation_item_id:06d}"
            )

        # Build the QR payload from saved database records
        qr_payload = {
            "purchase_order_id": purchase_order.purchase_order_id,
            "purchase_order_number": purchase_order.purchase_order_number,
            "preparation_id": preparation.preparation_id,
            "shipment_number": preparation.shipment_number,
            "expected_dispatch_date": (
                preparation.expected_dispatch_date.isoformat()
            ),
            "expected_delivery_date": (
                preparation.expected_delivery_date.isoformat()
            ),
            "items": [
                {
                    "product_id": item.product_id,
                    "prepared_quantity": item.prepared_quantity,
                    "batch_number": item.batch_number,
                    "manufacturing_date": (
                        item.manufacturing_date.isoformat()
                    ),
                    "expiry_date": (
                        item.expiry_date.isoformat()
                        if item.expiry_date else None
                    )
                }
                for item in preparation.preparation_items
            ]
        }

        # Generate QR image
        qr = qrcode.make(
            json.dumps(qr_payload)
        )

        image_buffer = io.BytesIO()
        qr.save(image_buffer, format="PNG")

        qr_base64 = base64.b64encode(
            image_buffer.getvalue()
        ).decode("utf-8")

        # Update statuses
        preparation.status = "Confirmed"
        purchase_order.status = "Prepared"

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "purchase_order_id": purchase_order.purchase_order_id,
        "purchase_order_number": purchase_order.purchase_order_number,
        "shipment_number": preparation.shipment_number,
        "status": preparation.status,
        "purchase_order_status": purchase_order.status,
        "items": qr_payload["items"],
        "qr_code": f"data:image/png;base64,{qr_base64}"
    }