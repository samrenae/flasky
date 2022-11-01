from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.bike import Bike


bike_bp = Blueprint("bike_bp", __name__, url_prefix="/bike")

def get_one_bike_or_abort(bike_id):
    try:
        bike_id = int(bike_id)
    except ValueError:
        response_str = f"Invalid bike_id: `{bike_id}`. ID must be an integer."
        abort(make_response(jsonify({"message":response_str}), 400))
    
    matching_bike = Bike.query.get(bike_id)

    if matching_bike is None:
        response_str = f"Bike with id `{bike_id}` was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 400))
    
    return matching_bike

@bike_bp.route("", methods=["POST"])
def add_bike():
    request_body = request.get_json()

    new_bike = Bike(
        name=request_body["name"],
        price=request_body["price"],
        size=request_body["size"],
        type=request_body["type"]
    )

    db.session.add(new_bike)
    db.session.commit()

    return {"id": new_bike.id}, 201

@bike_bp.route("", methods=["GET"])
def get_all_bikes():
    name_param = request.args.get("name")

    if name_param is None:
        bikes = Bike.query.all()
    else:
        bikes = Bike.query.filter_by(name=name_param)
        
    response = []
    for bike in bikes:
        bike_dict = {
            "id": bike.id,
            "name": bike.name,
            "price": bike.price,
            "size": bike.size,
            "type": bike.type
        }
        response.append(bike_dict)
    return jsonify(response), 200

#October 31
#Add DELETE, PUT, and GET(one bike)

@bike_bp.route("/<bike_id>", methods=["GET"])
def get_one_bike(bike_id):
    chosen_bike = get_one_bike_or_abort(bike_id)
    bike_dict = {
        "id": chosen_bike.id,
        "name": chosen_bike.name,
        "price": chosen_bike.price,
        "size": chosen_bike.size,
        "type": chosen_bike.type
    }

    return jsonify(bike_dict), 200

@bike_bp.route("/<bike_id>", methods=["PUT"])
def update_bike_with_new_vals(bike_id):
    chosen_bike = get_one_bike_or_abort(bike_id)

    request_body = request.get_json()

    if "name" not in request_body or \
        "size" not in request_body or \
        "price" not in request_body or \
        "type" not in request_body:
            return jsonify({"message": "Request must include name, size, price, and type"}), 400
    
    chosen_bike.name = request_body["name"]
    chosen_bike.size = request_body["size"]
    chosen_bike.price = request_body["price"]
    chosen_bike.type = request_body["type"]

    db.session.commit()

    return jsonify({"message": f"Successfully replaced bike with id `{bike_id}`"}), 200

@bike_bp.route("/<bike_id>", methods=["DELETE"])
def delete_one_bike(bike_id):
    chosen_bike = get_one_bike_or_abort(bike_id)
    db.session.delete(chosen_bike)

    db.session.commit()

    return jsonify({"message": f"Successfully deleted bike with id `{bike_id}`"}), 200

#Nov 1st
#Add Query params

