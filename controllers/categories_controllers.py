from flask import Flask, request, jsonify
import services.categories_services as categories_services

def create_catgories():
    #Request receive karna
    data = request.get_json()

    #Request se data extract karna
    name = data.get("name")

    #servie ko call karna

    get_service_res = categories_services.create_categories(name)

    #HTTP Response return karna
    if get_service_res is None:
        return jsonify({
            "message":"Category already exists"
        }), 409
    else:
        '''return jsonify({
            "message":"Category created successfully",
            "data":get_service_res
        }), 201'''
        return jsonify({
        "message": "Category created successfully",
        "data": {
            "category_id": get_service_res.category_id,
            "name": get_service_res.name
            }
        }), 201


def get_category():
    show_cat = categories_services.get_category()

    converted_category = []
    for category in show_cat:
        converted_category.append(category.to_dict())
    
    return jsonify({
            "message": "Categories fetched successfully",
            "data": converted_category
    }), 200


def get_specific_category(category_id):

    get_specific_cat = categories_services.get_specific_category(category_id)

    if get_specific_cat is None:
        return jsonify({
                    "message":"Category Not exists"
                }), 404

    return jsonify({
        "message":"Category found",
        "data": get_specific_cat.to_dict()
    }), 200

from flask import request, jsonify
from services import categories_services


def update_category(category_id):

    # Request receive
    data = request.get_json()

    # Data extract
    name = data.get("name")

    # Service call
    update_cat = categories_services.update_category(name, category_id)

    # Category not found
    if update_cat is None:
        return jsonify({
            "message": "Category not found"
        }), 404

    # Duplicate category
    if update_cat == "duplicate":
        return jsonify({
            "message": "Category already exists"
        }), 409

    # Success
    return jsonify({
        "message": "Category updated successfully",
        "data": update_cat.to_dict()
    }), 200




from flask import jsonify
from services import categories_services


def delete_category(category_id):

    # Service call
    del_cat = categories_services.delete_category(category_id)

    # Category not found
    if del_cat is None:
        return jsonify({
            "message": "Category not found"
        }), 404

    # Category is in use
    if del_cat == "Cannot delete, beacause product already using this category":
        return jsonify({
            "message": "Cannot delete category because it is assigned to one or more products."
        }), 409

    # Success
    return jsonify({
        "message": "Category deleted successfully",
        "data": del_cat.to_dict()
    }), 200

    
