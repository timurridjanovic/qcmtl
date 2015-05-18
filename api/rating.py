
from google.appengine.ext import ndb

#import main handler
from qcmtl import Handler

#import error messages
from qcmtl import error_messages

#import models
from models.vehicle_model import VehicleModel
from models.user_model import UserModel
from models.ride_model import RideModel

#import utilities
import logging
import re
import datetime
import cgi

class RatingList(Handler):
    def get(self, version, user_id):
        """
        Get list of all ratings per user_id
        """
        user = self.valid_user_id(user_id)
        
        ratings = RatingModel.get_ratings_by_user_id(user_id)
        json_obj = self.query_to_json(ratings, 'ratings')
        self.render_json(json_obj)

    def get_all_ratings(self, version):
        """
        Get list of all ratings
        """
        ratings = RatingModel.query()
        json_obj = self.query_to_json(ratings, 'ratings')
        self.render_json(json_obj)


    def post(self, version, user_id):
        """
        Creation of new rating for user_id
        """
        ride_id = self.request.get('ride_id')
        ride = self.valid_ride_id(ride_id, user_id)



class Rating(RatingList):
    def get(self, version, user_id, rating_id):
        """
        Get rating by id for user_id
        """
        logging.error("Get rating by id for user_id")

    def get_by_id(self, version, rating_id):
        """
        Get rating by id (without user_id)
        """
        logging.error("Get rating by id (without user_id)")


    def put(self, version, user_id, rating_id):
        """
        update existing rating for user_id
        """
        pass


    def delete(self, version, user_id, rating_id):
        """
        delete existing rating for user_id
        """
        pass


    def post(self, version, user_id, rating_id):
        """
        same as put
        """
        self.put(version, user_id, rating_id)


