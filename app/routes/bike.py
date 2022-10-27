from flask import Blueprint, jsonify

class Bike():
    def __init__(self, id, name, price, size, type):
        self.id = id
        self.name = name
        self.price = price
        self.size = size
        self.type = type
    
bikes = [
    Bike(5, "Nina", 100, 48, "gravel"),
    Bike(8, "Bike 3000", 1000, 50, "hybrid"),
    Bike(2, "Auberon", 2000, 52, "electronic")
]

bike_bp = Blueprint("bike_bp", __name__, url_prefix="/bike")

@bike_bp.route("", methods=["GET"])
def get_all_bikes():
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

@bike_bp.route("/<bike_id>", methods=["GET"])
def get_one_bike(bike_id):
    #see if bike_id can be converted to an integer
    #try-except: try to convert to an int, if error occurs, catch it and raise 400 error with message
    try:
        bike_id = int(bike_id)
    except ValueError:
        response_str = f"Invalid bike_id: `{bike_id}`. ID must be an integer"
        return jsonify({"message": response_str}), 400
    #after the try-except: bike_id will be a valid int

    #looping through data to find a bike with matching bike_id
    #if found: return that bikes data with 200 response code
    for bike in bikes:
        if bike.id == bike_id:
            bike_dict = {
                "id": bike.id,
                "name": bike.name,
                "price": bike.price,
                "size": bike.size,
                "type": bike.type
            }
            #return in the if block
            return jsonify(bike_dict), 200

    #after the loop: the bike with matching bike_id was not found, we will raise a 404 error with message
    response_message = f"bike_id: {bike_id} not found."
    return jsonify({"message": response_message}), 404