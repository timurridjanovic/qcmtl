from google.appengine.ext import ndb

#import models
from models.user_model import UserModel

class TokenModel(ndb.Model):
    """
    model for user tokens
    """
    user_key = ndb.KeyProperty(kind=UserModel, required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_token(self, user_key):
        """
        class method to create a ride
        """
        return TokenModel(user_key=user_key)
    
    @classmethod
    def get_user_for_token(self, token):
        return TokenModel.get_by_id(int(token))
