
from google.appengine.ext import ndb

#import models
from models.user_model import UserModel
from models.vehicle_model import VehicleModel

class RideModel(ndb.Model):
    """
    model of a ride (one user gives many rides) 
    """
    user_key = ndb.KeyProperty(kind=UserModel, required=True)
    vehicle_key = ndb.KeyProperty(kind=VehicleModel, required=True)
    available_seats = ndb.IntegerProperty(required=True)
    luggage_options = ndb.StringProperty(required=True)
    smoking_allowed = ndb.BooleanProperty(required=True)
    animal_options = ndb.StringProperty(required=True)
    comments = ndb.StringProperty()
    datetime = ndb.DateTimeProperty(required=True)
    departure_point = ndb.StringProperty(required=True)
    departure_city = ndb.StringProperty(required=True)
    destination_point = ndb.StringProperty(required=True)
    destination_city = ndb.StringProperty(required=True)
    num_of_reservations = ndb.IntegerProperty(default=0)
    passenger_ids = ndb.StringProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_ride(self, user_key, vehicle_key, available_seats, luggage_options, smoking_allowed, animal_options, datetime, departure_point,
            departure_city, destination_point, destination_city, comments=None):
        """
        class method to create a ride
        """
        return RideModel(user_key=user_key, vehicle_key=vehicle_key, available_seats=available_seats, luggage_options=luggage_options,
                smoking_allowed=smoking_allowed, animal_options=animal_options, comments=comments, datetime=datetime, departure_point=departure_point,
                departure_city=departure_city, destination_point=destination_point, destination_city=destination_city)
    
    
    @classmethod
    def get_ride_by_id(self, uid):
        return RideModel.get_by_id(int(uid))

    @classmethod
    def get_rides_by_user_id(self, user_id):
        return RideModel.query(RideModel.user_key==ndb.Key(UserModel, int(user_id)))
