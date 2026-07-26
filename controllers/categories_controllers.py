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