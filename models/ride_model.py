
from google.appengine.ext import ndb

#import models
from models.user_model import UserModel

class RideModel(ndb.Model):
    """
    model of a ride (one user gives many rides) 
    """
    user_key = ndb.KeyProperty(kind=UserModel, required=True)
    number_of_passengers = ndb.IntegerProperty(required=True)
    smoking_not_allowed = ndb.BooleanProperty(required=True)
    pets_not_allowed = ndb.BooleanProperty(required=True)
    car_description = ndb.StringProperty(required=True)
    additional_details = ndb.StringProperty()
    datetime = ndb.DateTimeProperty(required=True)
    departure_point = ndb.StringProperty(required=True)
    departure_city = ndb.StringProperty(required=True)
    destination_point = ndb.StringProperty(required=True)
    destination_city = ndb.StringProperty(required=True)
    num_of_reservations = ndb.IntegerProperty(default=0)
    passenger_ids = ndb.StringProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_ride(self, user_key, number_of_passengers, smoking_not_allowed, pets_not_allowed, car_description, datetime,
            additional_details, departure_point, departure_city, destination_point, destination_city):
        """
        class method to create a ride
        """
        return RideModel(user_key=user_key, number_of_passengers=number_of_passengers, smoking_not_allowed=smoking_not_allowed,
                pets_not_allowed=pets_not_allowed, datetime=datetime, car_description=car_description, additional_details=additional_details,
                departure_point=departure_point, departure_city=departure_city, destination_point=destination_point, destination_city=destination_city)
    
    
    @classmethod
    def get_ride_by_id(self, uid):
        return RideModel.get_by_id(int(uid))

    @classmethod
    def get_rides_by_user_id(self, user_id):
        return RideModel.query(RideModel.user_key==ndb.Key(UserModel, int(user_id)))
