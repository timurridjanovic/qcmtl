
from google.appengine.ext import ndb

#import models
from models.user_model import UserModel
from models.vehicle_model import VehicleModel
from models.ride_model import RideModel

class RatingModel(ndb.Model):
    """
    model of a rating (one user has many ratings)
    """
    ride_key = ndb.KeyProperty(kind=RideModel, required=True)
    user_key = ndb.KeyProperty(kind=UserModel, required=True)
    rater = ndb.StringProperty(required=True)
    punctuality_score = ndb.IntegerProperty(required=True)
    reliability_score = ndb.IntegerProperty(required=True)
    safety_score = ndb.IntegerProperty(required=True)
    total_score = ndb.IntegerProperty(required=True)
    comment = ndb.StringProperty()
    driver = ndb.BooleanProperty(required=True)

    @classmethod
    def create_rating(self, ride_key, user_key, rater, punctuality_score, reliability_score, safety_score, total_score, comment, driver):
        """
        class method to create a rating
        """
        return RatingModel(ride_key=ride_key, user_key=user_key, rater=rater, punctuality_score=punctuality_score, reliability_score=reliability_score,
                safety_score=safety_score, total_score=total_score, comment=comment, driver=driver)

    @classmethod
    def get_rating_by_id(self, uid):
        return RatingModel.get_by_id(int(uid))

    @classmethod
    def get_ratings_by_user_id(self, user_id):
        return RatingModel.query(RatingModel.user_key==ndb.Key(UserModel, int(user_id)))
