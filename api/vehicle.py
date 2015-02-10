
#import main handler
from qcmtl import Handler

#import error messages
from qcmtl import error_messages

#import models
from models.vehicle_model import VehicleModel

#import utilities
import logging


class VehicleList(Handler):
    def get(self, version, user_id):
        """
        Get list of all vehicles per user_id
        """
        user = self.valid_user_id(user_id)
        
        vehicles = VehicleModel.query(ancestor=user.key).fetch()
        json_obj = self.query_to_json(vehicles, 'vehicles')
        self.render_json(json_obj)

    def get_all_vehicles(self, version):
        """
        Get list of all vehicles
        """
        query = VehicleModel.query()
        json_obj = self.query_to_json(query, 'vehicles')
        self.render_json(json_obj)

    def post(self, version, user_id):
        """
        Creation of new vehicle for user_id
        """
        user = self.valid_user_id(user_id)

        license_number = self.request.get('license_number')
        winter_tires = self.json_to_bool(self.request.get('winter_tires')) #bool
        brand = self.request.get('brand')
        year = self.request.get('year')
        model = self.request.get('model')
        color = self.request.get('color')

        errors = self.validate_input(user_key=user.key, license_number=license_number, winter_tires=winter_tires, brand=brand, year=year, model=model, color=color)

        if errors.keys():
            self.throw_json_error({
                "error_types": errors,
                error_messages['error_key']: error_messages['input_error']
            })
            return

        new_vehicle = VehicleModel.create_vehicle(user_id=int(user_id), license_number=license_number, winter_tires=winter_tires, brand=brand, year=year, 
                model=model, color=color)

        key = new_vehicle.put()

        self.render_json({
            'url': '/api/' + self.api_version + '/users/' + user_id + '/vehicles/' + str(key.id()),
            'vehicles': self.query_to_json([new_vehicle], None)
        })


    def validate_input(self, user_key, license_number, winter_tires, brand, year, model, color):
        """
        TODO: maybe validate license number? for now, we'll just check whether they exist
        """
        errors = {}
        if not license_number:
            errors['license_number_error'] = "You haven't provided a valid license number."
        if not self.unique_license(user_key, license_number):
            errors['unique_license_error'] = "This user already has a registered vehicle with this license."
        if not winter_tires == True and not winter_tires == False: #bool
            errors['winter_tires_error'] = "You haven't told us whether your vehicle has winter tires."
        if not brand:
            errors['brand_error'] = "You haven't provided the brand of the vehicle."
        if not year:
            errors['year_error'] = "You haven't provided the year of the vehicle."
        if not model:
            errors['model_error'] = "You haven't provided the model of the vehicle."
        if not color:
            errors['color_error'] = "You haven't provided the color of the vehicle."
        return errors

    def unique_license(self, user_key, license_number):
        query = VehicleModel.query(ancestor=user_key).filter(VehicleModel.license_number == license_number)
        return not query.get()



class Vehicle(VehicleList):
    def get(self, version, user_id, vehicle_id):
        """
        Get vehicle by id for user_id
        """
        vehicle = self.valid_vehicle_id(vehicle_id, user_id)
        json_obj = self.query_to_json([vehicle], 'vehicles')
        self.render_json(json_obj)

    def get_by_id(self, version, vehicle_id):
        """
        Get vehicle by id (doesn't work because we need the user_id to make that query)
        """
        self.throw_json_error({error_messages['error_key']: error_messages['vehicle_id_without_userid_error']})
        

    def put(self, version, user_id, vehicle_id):
        """
        update existing vehicle for user_id
        """
        vehicle = self.valid_vehicle_id(vehicle_id, user_id)

        license_number = self.check_empty_string(self.request.get('license_number'))
        winter_tires = self.check_empty_string(self.request.get('winter_tires')) #bool
        brand = self.check_empty_string(self.request.get('brand'))
        year = self.check_empty_string(self.request.get('year'))
        model = self.check_empty_string(self.request.get('model'))
        color = self.check_empty_string(self.request.get('color'))

        fields_to_update, errors = self.validate_put_input(license_number=license_number, winter_tires=winter_tires, brand=brand, year=year, model=model,
                color=color)

        if errors.keys():
            self.throw_json_error({
                "error_types": errors,
                error_messages['error_key']: error_messages['input_error']
            })
            return

        new_vehicle = self.put_update(vehicle, fields_to_update)

        new_vehicle.put()
        json_obj = self.query_to_json([new_vehicle], 'vehicles')
        self.render_json(json_obj)


    def delete(self, version, user_id, vehicle_id):
        """
        delete existing vehicle for user_id
        """
        vehicle = self.valid_vehicle_id(vehicle_id, user_id)
        
        vehicle.key.delete()
        self.render_json({
            "response": "vehicle " + vehicle_id + " was deleted successfully",
            "vehicles": self.query_to_json([vehicle], None)
        })

    def post(self, version, user_id, vehicle_id):
        """
        same as put
        """
        self.put(version, user_id, vehicle_id)

    def validate_put_input(self, license_number, winter_tires, brand, year, model, color):
        """
        validate data for update on put
        Note: if parameters are equal to None, that means that they were empty strings (properties the user did not want to update) and thus we just ignore that
        """
        fields_to_update = {}
        errors = {}
        if not license_number == None:
            fields_to_update['license_number'] = license_number
        if not winter_tires == None:
            winter_tires = self.json_to_bool(winter_tires) #bool
            if winter_tires == True or winter_tires == False: 
                fields_to_update['winter_tires'] = winter_tires
            else:
                errors['winter_tires_error'] = "This property should be a boolean."
        if not brand == None:
            fields_to_update['brand'] = brand
        if not year == None:
            fields_to_update['year'] = year
        if not model == None:
            fields_to_update['model'] = model
        if not color == None:
            fields_to_update['color'] = color
        return fields_to_update, errors

