from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.bike import Bike
from .routes_helper import get_one_obj_or_abort

bike_bp = Blueprint("bike_bp", __name__, url_prefix="/bike")


@bike_bp.route("", methods=["POST"])
def add_bike():
    request_body = request.get_json()

    new_bike = Bike.from_dict(request_body)

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

    
    response = [bike.to_dict() for bike in bikes]
    return jsonify(response), 200

#October 31
#Add DELETE, PUT, and GET(one bike)

@bike_bp.route("/<bike_id>", methods=["GET"])
def get_one_bike(bike_id):
    chosen_bike = get_one_obj_or_abort(Bike, bike_id)

    bike_dict = chosen_bike.to_dict()

    return jsonify(bike_dict), 200

@bike_bp.route("/<bike_id>", methods=["PUT"])
def update_bike_with_new_vals(bike_id):
    chosen_bike = get_one_obj_or_abort(Bike, bike_id)

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
    chosen_bike = get_one_obj_or_abort(Bike, bike_id)
    db.session.delete(chosen_bike)

    db.session.commit()

    return jsonify({"message": f"Successfully deleted bike with id `{bike_id}`"}), 200

#Nov 1st
#Add Query params

