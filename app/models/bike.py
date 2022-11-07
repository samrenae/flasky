from app import db

class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    size = db.Column(db.Integer)
    type = db.Column(db.String)

    def to_dict(self):
        bike_dict = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "size": self.size,
            "type": self.type
        }
        return bike_dict

    @classmethod
    def from_dict(cls, data_dict):
        if "name" in data_dict and "price" in data_dict and "size" in data_dict and "type" in data_dict:
            new_obj=cls(name=data_dict["name"],
            price=data_dict["price"],
            size=data_dict["size"],
            type=data_dict["type"])

            return new_obj
