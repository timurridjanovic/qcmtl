
import webapp2
import os
import jinja2
import logging
import json
import datetime

#import models
from models.user_model import UserModel
from models.vehicle_model import VehicleModel
from models.ride_model import RideModel

template_dir = os.path.join(os.path.dirname(__file__), 'front-end/build')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

error_messages = {
    'error_key': 'error',
    'user_id_error': 'this user id does not exist.',
    'vehicle_id_error': 'this vehicle id does not exist.',
    'api_version_error': 'the api version is not valid. Please use v1.',
    'input_error': 'this is an input validation error. Look at the error_types property for more details.',
    'http_method_data_error': 'this entity does not have the properties you wish to change. Please do not use nested dicts.',
    'vehicle_id_without_userid_error': 'we do not give specific vehicle info without a provided userid.',
    'ride_id_error': 'this ride id does not exist.',
    'ride_user_id_error': 'this ride id does not correspond with this user id.',
    'update_type_error': 'the item you are trying to update is of the wrong type.'
}

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        pass

    def initialize(self, request, response):
        """
        method gets called before each request
        """
        webapp2.RequestHandler.initialize(self, request, response)
        uri_params = filter(lambda x: True if x else False, request.path.split('/'))
        if self.is_api_call(uri_params):
            self.api_version = self.valid_api_version(uri_params)
            if not self.api_version:
                self.abort(404, detail=error_messages['api_version_error'])


    def is_api_call(self, uri_params):
        """
        checks to see if request is an api request
        """
        if uri_params and uri_params[0] == 'api':
            return True
        return False

    def valid_api_version(self, uri_params):
        """
        requires url_path to have this format: /api/version_number/... (with optional slash at the beginning)
        """
        api_version = uri_params[1]
        if api_version != 'v1':
            return None
        return api_version


    def throw_json_error(self, msg_obj):
        """ 
        same as render_json method, but for semantic purposes the name was changed
        """
        self.render_json(msg_obj)

    def render_json(self, json_obj):
        """
        utility method to send json response to browser
        """
        self.response.headers['Content-type'] = 'application-json'
        self.write(json.dumps(json_obj))


    def query_to_json(self, query, key, hidden_fields=['password']):
        """
        utility method to transform entity query into dictionary that can then be transformed into json
        """
        result = []
        for entry in query:
            json_dict = {}
            for k in entry._values.keys():
                if k not in hidden_fields:
                    value = getattr(entry, k)
                    (new_key, new_value) = self._process_value_for_json(k, value) 
                    json_dict[new_key] = new_value
            json_dict['id'] = entry.key.id()
            result.append(json_dict)
        if key == None:
            return result
        return {key: result}

    def _process_value_for_json(self, key, value):
        #value is key
        if hasattr(value, 'id'):
            return (key.replace('key', 'id'), value.id())
        if type(value) == datetime.datetime or type(value) == datetime.date:
            return (key, str(value))
        return (key, value)

    def json_to_int(self, number_string, default=True):
        """
        utility method to transform input json strings into python parsable types
        """
        if number_string.isdigit():
            return int(number_string)
        if default:
            return 0
        return None

    def json_to_bool(self, bool_string):
        """
        utility method to transform input json strings into python parsable types
        """
        if bool_string == 'true':
            return True
        return False

    def json_to_date(self, date_string):
        """
        utility method to transform input json strings into python parsable types
        """
        if date_string.isdigit():
            return datetime.datetime.fromtimestamp(int(date_string)/1000)
        return None

    def json_to_picture_uri(self, picture_url):
        """
        utility method to transform input json strings into python parsable types
        """
        if not picture_url or picture_url == 'null':
            return None
        return picture_url

    def json_to_list(self, l):
        """
        utility method to transform input json into python list
        """
        if type(l) == list:
            return l
        if type(l) == dict:
            return l.values()
        if type(l) == int:
            return [l]
        if l.isdigit():
            return [l]
        return None

    def check_empty_string(self, string):
        """
        utility method to check empty string. Returns None is empty string.
        """
        if string == "":
            return None
        return string

    def check_empty_list(self, l):
        """
        utility method to check empty lists. Returns None if empty list.
        """
        if len(l) <= 0 or type(l) != list:
            return None
        return l


    def valid_user_id(self, user_id):
        """
        this is a utility method for when you just want to check if the user_id is valid. If it is valid, it returns the entity
        """
        user = UserModel.get_user_by_id(user_id)
        if not user:
            self.abort(404, detail=error_messages['user_id_error'])
            return False
        return user

    def valid_vehicle_id(self, vehicle_id, user_id):
        """
        this is a utility method for when you just want to check if the vehicle_id is valid. If it is valid, it returns the entity
        """
        vehicle = VehicleModel.get_vehicle_by_id(vehicle_id, user_id)
        if not vehicle:
            if self.valid_user_id(user_id):
                self.abort(404, detail=error_messages['vehicle_id_error'])
            else:
                self.abort(404, detail=error_messages['user_id_error'])
            return False
        return vehicle

    def valid_ride_id(self, ride_id, user_id=None):
        """
        this is a utility method for when you just want to check if the ride_id is valid. If it is valid, it returns the entity
        """
        ride = RideModel.get_ride_by_id(ride_id)
        if ride:
            if not user_id:
                return ride
            if ride.user_key.id() == int(user_id):
                return ride
            else:
                if self.valid_user_id(user_id):
                    self.abort(404, detail=error_messages['ride_user_id_error'])
                else: 
                    self.abort(404, detail=error_messages['user_id_error'])
                return False
        self.abort(404, detail=error_messages['ride_id_error'])
        return False


    def put_update(self, entity, fields_to_update):
        """
        utility method to update entity on http PUT
        """
        for key in fields_to_update:
            value = fields_to_update[key]

            if not hasattr(entity, key):
                self.abort(403, detail=error_messages['http_method_data_error'])
                return False

            current_value = getattr(entity, key)
            if not type(current_value) == type(value):
                self.abort(403, detail=error_messages['update_type_error'])
                return False
            
            setattr(entity, key, value)
        return entity


class Index(Handler):
    def get(self):
        self.render('index.html')


application = webapp2.WSGIApplication([
    ('/', Index), #index html page
    webapp2.Route('/api/<version>/users<:(/?)>', handler='api.user.UserList'), #UserList
    webapp2.Route('/api/<version>/users/<user_id:(\w+)><:(/?)>', handler='api.user.User'), #User

    webapp2.Route('/api/<version>/vehicles<:(/?)>', handler='api.vehicle.VehicleList', handler_method='get_all_vehicles', methods=['GET']), #VehicleList
    webapp2.Route('/api/<version>/vehicles/<vehicle_id:(\w+)><:(/?)>', handler='api.vehicle.Vehicle', handler_method='get_by_id', methods=['GET']), #Vehicle (generates an error for now)
    webapp2.Route('/api/<version>/users/<user_id:(\w+)>/vehicles<:(/?)>', handler='api.vehicle.VehicleList'), #VehicleList per User
    webapp2.Route('/api/<version>/users/<user_id:(\w+)>/vehicles/<vehicle_id:(\w+)><:(/?)>', handler='api.vehicle.Vehicle'), #Vehicle per User

    webapp2.Route('/api/<version>/rides<:(/?)>', handler='api.ride.RideList', handler_method='get_all_rides', methods=['GET']), #RideList
    webapp2.Route('/api/<version>/rides/<ride_id:(\w+)><:(/?)>', handler='api.ride.Ride', handler_method='get_by_id', methods=['GET']), #Ride
    webapp2.Route('/api/<version>/users/<user_id:(\w+)>/rides<:(/?)>', handler='api.ride.RideList'), #RideList per User
    webapp2.Route('/api/<version>/users/<user_id:(\w+)>/rides/<ride_id:(\w+)><:(/?)>', handler='api.ride.Ride'), #Ride per User (same as Ride)

    webapp2.Route('/api/<version>/ratings<:(/?)>', handler='api.rating.RatingList', handler_method='get_all_ratings', methods=['GET']), #RatingList
    webapp2.Route('/api/<version>/ratings/<rating_id:(\w+)><:(/?)>', handler='api.rating.Rating', handler_method='get_by_id', methods=['GET']), #Rating
    webapp2.Route('/api/<version>/users/<user_id:(\w+)>/ratings<:(/?)>', handler='api.rating.RatingList'), #RatingList per User
    webapp2.Route('/api/<version>/users/<user_id:(\w+)>/ratings/<rating_id:(\w+)><:(/?)>', handler='api.rating.Rating'), #Rating per User (same as Rating)
    
    
], debug=True)


#error handlers
def handle_404(request, response, exception):
    handle_error(request, response, exception, 404)

def handle_403(request, response, exception):
    handle_error(request, response, exception, 403)

def handle_error(request, response, exception, status_code):
    response.headers['Content-type'] = 'application-json'
    response.out.write(json.dumps({
        error_messages['error_key']: str(exception),
        "status_code": status_code
    }))

application.error_handlers[404] = handle_404
application.error_handlers[403] = handle_403
