
from google.appengine.ext import ndb

#import models
from models.user_model import UserModel

class VehicleModel(ndb.Model):
    """
    model of a vehicle (one user owns many vehicles) 
    """
    user_key = ndb.KeyProperty(kind=UserModel, required=True)
    license_number = ndb.StringProperty(required=True)
    winter_tires = ndb.BooleanProperty(default=False)
    brand = ndb.StringProperty(required=True)
    year = ndb.StringProperty(required=True)
    model = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_vehicle(self, user_id, license_number, winter_tires, brand, year, model, color):
        """
        class method to create new vehicle
        """
        user_key = UserModel.get_user_key(user_id)
        return VehicleModel(parent=vehicle_ancestor_key(user_id), user_key=user_key, license_number=license_number, winter_tires=winter_tires, 
                brand=brand, year=year, model=model, color=color)


    @classmethod
    def get_vehicle_by_id(self, uid, user_id):
        if uid.isdigit() and user_id.isdigit():
            return VehicleModel.get_by_id(int(uid), parent=vehicle_ancestor_key(int(user_id)))
        return None


#VehicleModel utility functions

def vehicle_ancestor_key(user_id):
    return ndb.Key('UserModel', int(user_id))

