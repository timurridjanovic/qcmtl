
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

class RideList(Handler):
    def get(self, version, user_id):
        """
        Get list of all rides per user_id
        """
        user = self.valid_user_id(user_id)
        
        rides = RideModel.get_rides_by_user_id(user_id)
        json_obj = self.query_to_json(rides, 'rides')
        self.render_json(json_obj)

    def get_all_rides(self, version):
        """
        Get list of all rides
        """
        rides = RideModel.query()
        json_obj = self.query_to_json(rides, 'rides')
        self.render_json(json_obj)

    def post(self, version, user_id):
        """
        Creation of new ride for user_id
        """
        user = self.valid_user_id(user_id)
        vehicle_id = self.request.get('vehicle_id')
        vehicle = self.valid_vehicle_id(vehicle_id, user_id)

        available_seats = self.json_to_int(self.request.get('available_seats')) #int
        luggage_options = self.request.get('luggage_options')
        smoking_allowed = self.json_to_bool(self.request.get('smoking_allowed')) #bool
        animal_options = self.request.get('animal_options')
        comments = self.request.get('comments')
        datetime = self.json_to_date(self.request.get('datetime')) #date
        departure_point = self.request.get('departure_point')
        departure_city = self.request.get('departure_city')
        destination_point = self.request.get('destination_point')
        destination_city = self.request.get('destination_city')
        num_of_reservations = self.json_to_int(self.request.get('num_of_reservations')) #int
        passenger_ids = self.json_to_list(self.request.get('passenger_ids')) #list

        errors = self.validate_input(available_seats=available_seats, luggage_options=luggage_options,
                smoking_allowed=smoking_allowed, datetime=datetime, departure_point=departure_point, departure_city=departure_city,
                destination_point=destination_point, destination_city=destination_city)

        if errors.keys():
            self.throw_json_error({
                "error_types": errors,
                error_messages['error_key']: error_messages['input_error']
            })
            return

        new_ride = RideModel.create_ride(user_key=user.key, vehicle_key=vehicle.key, available_seats=available_seats, luggage_options=luggage_options,
                smoking_allowed=smoking_allowed, animal_options=animal_options, comments=comments, datetime=datetime, departure_point=departure_point,
                departure_city=departure_city, destination_point=destination_point, destination_city=destination_city)
        
        key = new_ride.put()

        self.render_json({
            'url': '/api/' + self.api_version + '/users/' + user_id + '/rides/' + str(key.id()),
            'rides': self.query_to_json([new_ride], None)
        })


    def validate_input(self, available_seats, luggage_options, smoking_allowed, datetime, departure_point, departure_city,
            destination_point, destination_city):
        errors = {}
        if not available_seats:
            errors['available_seats_error'] = "You haven't provided the number of available seats in the vehicle."
        if not luggage_options:
            errors['luggage_options_error'] = "You haven't provided luggage options."
        if not smoking_allowed == True and not smoking_allowed == False: #bool
            errors['smoking_allowed_error'] = "You haven't provided the smoking allowed boolean."
        if not datetime:
            errors['datetime_error'] = "You have not provided a date and time for the ride."
        if not departure_point:
            errors['departure_point_error'] = "You have not provided a departure point for the ride."
        if not departure_city:
            errors['departure_city_error'] = "You haven't provided a departure city for the ride."
        if not destination_point:
            errors['destination_point_error'] = "You haven't provided a destination point for the ride"
        if not destination_city:
            errors['destination_city_error'] = "You haven't provided a destination city for the ride"
        return errors
    


class Ride(RideList):
    def get(self, version, user_id, ride_id):
        """
        Get ride by id for user_id
        """
        ride = self.valid_ride_id(ride_id, user_id)
        json_obj = self.query_to_json([ride], 'rides')
        self.render_json(json_obj)
        
    def get_by_id(self, version, ride_id):
        """
        Get ride by id (without user_id)
        """
        ride = self.valid_ride_id(ride_id)
        json_obj = self.query_to_json([ride], 'rides')
        self.render_json(json_obj)

    def put(self, version, user_id, ride_id):
        """
        update existing ride for user_id
        """
        ride = self.valid_ride_id(ride_id, user_id)
        
        vehicle_id = self.check_empty_string(self.request.get('vehicle_id')) #int
        available_seats = self.check_empty_string(self.request.get('available_seats')) #int
        luggage_options = self.check_empty_string(self.request.get('luggage_options'))
        smoking_allowed = self.check_empty_string(self.request.get('smoking_allowed')) #bool
        animal_options = self.check_empty_string(self.request.get('animal_options'))
        comments = self.check_empty_string(self.request.get('comments'))
        datetime = self.check_empty_string(self.request.get('datetime')) #date
        departure_point = self.check_empty_string(self.request.get('departure_point'))
        departure_city = self.check_empty_string(self.request.get('departure_city'))
        destination_point = self.check_empty_string(self.request.get('destination_point'))
        destination_city = self.check_empty_string(self.request.get('destination_city'))
        num_of_reservations = self.check_empty_string(self.request.get('num_of_reservations')) #int
        passenger_ids = self.check_empty_list(self.request.POST.getall('passenger_ids[]')) #list

        fields_to_update, errors = self.validate_put_input(user_id=user_id, vehicle_id=vehicle_id, available_seats=available_seats, 
                luggage_options=luggage_options, smoking_allowed=smoking_allowed, animal_options=animal_options, comments=comments, datetime=datetime, 
                departure_point=departure_point, departure_city=departure_city, destination_point=destination_point, destination_city=destination_city,
                num_of_reservations=num_of_reservations, passenger_ids=passenger_ids)

        if errors.keys():
            self.throw_json_error({
                "error_types": errors,
                error_messages['error_key']: error_messages['input_error']
            })
            return

        new_ride = self.put_update(ride, fields_to_update)

        new_ride.put()
        json_obj = self.query_to_json([new_ride], 'rides')
        self.render_json(json_obj)

    def delete(self, version, user_id, ride_id):
        """
        delete existing ride for user_id
        """
        ride = self.valid_ride_id(ride_id, user_id)
        
        ride.key.delete()
        self.render_json({
            "response": "ride " + ride_id + " was deleted successfully",
            "rides": self.query_to_json([ride], None)
        })
    
    def post(self, version, user_id, ride_id):
        """
        same as put
        """
        self.put(version, user_id, ride_id)
    
    
    def validate_put_input(self, user_id, vehicle_id, available_seats, luggage_options, smoking_allowed, animal_options, comments, datetime, departure_point,
            departure_city, destination_point, destination_city, num_of_reservations, passenger_ids):
        """
        method to validate data to be updated on put
        Note: if parameters are equal to None, that means that they were empty strings (properties the user did not want to update) and thus we just ignore that
        """
        fields_to_update = {}
        errors = {}
        if not vehicle_id == None:
            if self.valid_vehicle_id(vehicle_id, user_id):
                fields_to_update['vehicle_id'] = vehicle_id
            else:
                errors['vehicle_id_error'] = "You haven't provided a valid vehicle id."
        if not available_seats == None:
            available_seats = self.json_to_int(available_seats, False)
            if available_seats:
                fields_to_update['available_seats'] = available_seats
            else:
                errors['available_seats_error'] = "The available_seats property needs to be an integer."
        if not luggage_options == None:
            fields_to_update['luggage_options'] = luggage_options
        if not smoking_allowed == None:
            smoking_allowed = self.json_to_bool(smoking_allowed) #bool
            if smoking_allowed == True or smoking_allowed == False:
                fields_to_update['smoking_allowed'] = smoking_allowed
            else:
                errors['smoking_allowed_error'] = "The smoking_allowed property needs to be a boolean."
        if not animal_options == None:
            fields_to_update['animal_options'] = animal_options
        if not comments == None:
            fields_to_update['comments'] = comments
        if not datetime == None:
            datetime = self.json_to_date(datetime) #date
            if datetime:
                fields_to_update['datetime'] = datetime
            else:
                errors['datetime_error'] = "The datetime property needs to be a javascript timestamp ex: new Date(date).getTime()."
        if not departure_point == None:
            fields_to_update['departure_point'] = departure_point
        if not departure_city == None:
            fields_to_update['departure_city'] = departure_city
        if not destination_point == None:
            fields_to_update['destination_point'] = destination_point
        if not destination_city == None:
            fields_to_update['destination_city'] = destination_city
        if not num_of_reservations == None:
            num_of_reservations = self.json_to_int(num_of_reservations)
            if num_of_reservations:
                fields_to_update['num_of_reservations'] = num_of_reservations
            else:
                errors['num_of_reservations_error'] = "The num_of_reservations property must be an integer."
        if not passenger_ids == None:
            passenger_ids = self.valid_passenger_ids(user_id, passenger_ids)
            if passenger_ids:
                fields_to_update['passenger_ids'] = passenger_ids
            else:
                errors['passenger_ids_error'] = "The passenger_ids you provided are not valid."
        return fields_to_update, errors
            
    def valid_passenger_ids(self, user_id, passenger_ids):
        passenger_ids = self.json_to_list(passenger_ids)
        if passenger_ids:
            for passenger in passenger_ids:
                user = self.valid_user_id(passenger)
                if str(user_id) == str(passenger):
                    return False
            return passenger_ids
        return False
