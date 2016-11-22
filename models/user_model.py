
from google.appengine.ext import ndb

#utility imports
import random 
from string import letters
import hashlib

class UserModel(ndb.Model):
    """
        Model of a user
    """
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    credits = ndb.IntegerProperty(default=0)
    driver = ndb.BooleanProperty(default=False)
    drivers_license = ndb.StringProperty()
    profile_picture = ndb.BlobProperty()
    number_of_rides = ndb.IntegerProperty(default=0)
    years_of_experience = ndb.IntegerProperty(default=0)
    phone_verified = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)


    @classmethod
    def create_user(self, email, password, first_name, last_name, phone, credits=0, 
            driver=False, drivers_license=None, profile_picture=None, number_of_rides=0, years_of_experience=0):
        """
            class method to create user
        """
        password_hash = make_password_hash(email, password)
        return UserModel(email=email, password=password_hash, first_name=first_name, last_name=last_name, 
                phone=phone, credits=credits, driver=driver, drivers_license=drivers_license, 
                profile_picture=profile_picture, number_of_rides=number_of_rides, 
                years_of_experience=years_of_experience)

    @classmethod
    def get_user_by_id(self, uid):
        return UserModel.get_by_id(int(uid))

    @classmethod
    def get_user_key(self, uid):
        return ndb.Key(UserModel, int(uid))

    @classmethod
    def hash_password(self, email, new_password):
        password_hash = maske_password_hash(email, new_password)
        return password_hash

    @classmethod
    def is_valid_email_and_password(self, email, password):
        user = UserModel.query(UserModel.email == email).get()
        if user:
            h = user.password
            if valid_password(email, password, h):
                return user
        return False



# utility functions for UserModel

def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_password_hash(username, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(username + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_password(username, password, h):
    salt = h.split(',')[0]
    return h == make_password_hash(username, password, salt)
