

#import main handler
from qcmtl import Handler

#import error messages
from qcmtl import error_messages

#import models
from models.user_model import UserModel

#import utilities
import logging
import re


class UserList(Handler):
    def get(self, version):
        """
        list all users
        """
        query = UserModel.query()
        json_obj = self.query_to_json(query, 'users')
        self.render_json(json_obj)


    def post(self, version):
        """
        create new user
        """
        email = self.request.get('email')
        password = self.request.get('password')
        first_name = self.request.get('first_name') 
        last_name = self.request.get('last_name')
        phone_number = self.request.get('phone_number')
        city = self.request.get('city')
        sex = self.request.get('sex')
        country = self.request.get('country')
        province = self.request.get('province')
        date_of_birth = self.json_to_date(self.request.get('date_of_birth')) #date
        student = self.json_to_bool(self.request.get('student')) #bool
        student_picture = self.json_to_picture_uri(self.request.get('student_picture')) #picture
        driver = self.json_to_bool(self.request.get('driver'))  #bool
        drivers_license = self.request.get('drivers_license')
        occupation = self.request.get('occupation')
        education = self.request.get('education')
        motto = self.request.get('motto')
        profile_picture = self.request.get('profile_picture')
        years_of_experience = self.json_to_int(self.request.get('years_of_experience')) #int

        errors = self.validate_input(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number,
                city=city, sex=sex, country=country, province=province, date_of_birth=date_of_birth, drivers_license=drivers_license)

        if errors.keys():
            self.throw_json_error({
                "error_types": errors,
                error_messages['error_key']: error_messages['input_error']
            })
            return


        new_user = UserModel.create_user(email=email, password=password, first_name=first_name, last_name=last_name, 
            phone_number=phone_number, city=city, sex=sex, province=province, country=country, date_of_birth=date_of_birth, 
            credits=0, student=student, student_picture=None, student_expiration_date=None,
            driver=driver, drivers_license=drivers_license, occupation=occupation, education=education, motto=motto, 
            profile_picture=profile_picture, years_of_experience=years_of_experience)

        key = new_user.put()

        self.render_json({
            'url': '/api/' + self.api_version + '/users/' + str(key.id()),
            'users': self.query_to_json([new_user], None)
        })



    def validate_input(self, email, password, first_name, last_name, phone_number, city, sex, country, province, date_of_birth, drivers_license):
        errors = {}
        if not self.unique_email(email):
            errors['unique_email_error'] = 'the email you provided is already registered'
        if not self.valid_email(email): 
            errors['email_error'] = 'the email address you provided is not valid'
        if not self.valid_password(password):
            errors['password_error'] = 'the password you provided is not valid. It must be between 8 and 20 characters long.'
        if not self.valid_date(date_of_birth):
            errors['date_error'] = 'the date of birth you provided is not valid. you must provide a timestamp with the getTime() method on the js date object.'
        return errors

       
    def unique_email(self, email):
        query = UserModel.query(UserModel.email == email)
        return not query.get()
        

    def valid_email(self, email):
        EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return email and EMAIL_RE.match(email)

    def valid_password(self, password):
        PASS_RE = re.compile(r"^.{8,20}$")
        return password and PASS_RE.match(password)

    def valid_date(self, date):
        if date:
            return True
        return False


class User(UserList):
    def get(self, version, user_id):
        """
        list user by id
        """
        user = self.valid_user_id(user_id)
        json_obj = self.query_to_json([user], 'users')
        self.render_json(json_obj)


    def put(self, version, user_id):
        """
        update existing user
        """
        user = self.valid_user_id(user_id)

        email = self.check_empty_string(self.request.get('email'))
        password = self.check_empty_string(self.request.get('password'))
        first_name = self.check_empty_string(self.request.get('first_name'))
        last_name = self.check_empty_string(self.request.get('last_name'))
        phone_number = self.check_empty_string(self.request.get('phone_number'))
        city = self.check_empty_string(self.request.get('city'))
        sex = self.check_empty_string(self.request.get('sex'))
        country = self.check_empty_string(self.request.get('country'))
        province = self.check_empty_string(self.request.get('province'))
        date_of_birth = self.check_empty_string(self.request.get('date_of_birth')) #date
        student = self.check_empty_string(self.request.get('student')) #bool
        student_picture = self.check_empty_string(self.request.get('student_picture')) #picture
        driver = self.check_empty_string(self.request.get('driver'))  #bool
        drivers_license = self.check_empty_string(self.request.get('drivers_license'))
        occupation = self.check_empty_string(self.request.get('occupation'))
        education = self.check_empty_string(self.request.get('education'))
        motto = self.check_empty_string(self.request.get('motto'))
        profile_picture = self.check_empty_string(self.request.get('profile_picture')) #picture
        years_of_experience = self.check_empty_string(self.request.get('years_of_experience')) #int

        fields_to_update, errors = self.validate_put_input(user=user, email=email, password=password, first_name=first_name, last_name=last_name, 
                phone_number=phone_number, city=city, sex=sex, country=country, province=province, date_of_birth=date_of_birth, student=student, 
                student_picture=student_picture, driver=driver, drivers_license=drivers_license, occupation=occupation, education=education, motto=motto, 
                profile_picture=profile_picture, years_of_experience=years_of_experience)

        if errors.keys():
            self.throw_json_error({
                "error_types": errors,
                error_messages['error_key']: error_messages['input_error']
            })
            return

        new_user = self.put_update(user, fields_to_update)

        new_user.put()
        json_obj = self.query_to_json([new_user], 'users')
        self.render_json(json_obj)

    def post(self, version, user_id):
        """
        allowing updates via post
        """
        self.put(version, user_id)


    def delete(self, version, user_id):
        """
        delete existing user
        """
        user = self.valid_user_id(user_id)
        
        user.key.delete()
        self.render_json({
            "response": "user " + user_id + " was deleted successfully",
            "users": self.query_to_json([user], None)
        })

    def validate_put_input(self, user, email, password, first_name, last_name, phone_number, city, sex, country, province, date_of_birth, student, 
            student_picture, driver, drivers_license, occupation, education, motto, profile_picture, years_of_experience):
        """
        validate data for update on put
        Note: if parameters are equal to None, that means that they were empty strings (properties the user did not want to update) and thus we just ignore that
        """
        fields_to_update = {}
        errors = {}
        if not email == None:
            if self.unique_email(email):
                #if changing email, must change password too
                if self.valid_password(password):
                    fields_to_update['email'] = email
                    fields_tp_update['password'] = UserModel.hash_password(email, password)
                else:
                    errors['email_password_update_error'] = "You must provide a new valid password with your new email."

                fields_to_update['email'] = email
            else:
                errors['unique_email_error'] = "The email you provided is already registered."
        else:
            if not password == None:
                if self.valid_password(password):
                    fields_to_update['password'] = UserModel.hash_password(user.email, password)
                else:
                    errors['password_error'] = "You must provide a valid new password."
        
        if not first_name == None:
            fields_to_update['first_name'] = first_name
        if not last_name == None:
            fields_to_update['last_name'] = last_name
        if not phone_number == None:
            fields_to_update['phone_number'] = phone_number
        if not city == None:
            fields_to_update['city'] = city
        if not sex == None:
            fields_to_update['sex'] = sex
        if not country == None:
            fields_to_update['country'] = country
        if not province == None:
            fields_to_update['province'] = province
        if not date_of_birth == None:
            date_of_birth = self.json_to_date(date_of_birth) #date
            if date:
                fields_to_update['date_of_birth'] = date_of_birth
            else:
                errors['date_of_birth_error'] = "This property needs to be a javascript timestamp ex: new Date(date).getTime()."
        if not student == None: 
            student = self.json_to_bool(student) #bool
            if student == True or student == False:
                fields_to_update['student'] = student
            else:
                errors['student_error'] = "This property should be a boolean."
        if not student_picture == None:
            student_picture = self.json_to_picture(student_picture)
            if student_picture:
                fields_to_update['student_picture'] = student_picture
            else:
                errors['student_picture_error'] = "this image is not valid."
        if not driver == None:
            driver = self.json_to_bool(driver) #bool
            if driver == True or driver == False:
                fields_to_update['driver'] = driver
            else:
                errors['driver_error'] = "This property should be a boolean."
        if not drivers_license == None:
            fields_to_update['drivers_license'] = drivers_license
        if not occupation == None:
            fields_to_update['occupation'] = occupation
        if not education == None:
            fields_to_update['education'] = education
        if not motto == None:
            fields_to_update['motto'] = motto
        if not profile_picture == None:
            profile_picture = self.json_to_picture(profile_picture)
            if profile_picture:
                fields_to_update['profile_picture'] = profile_picture
            else:
                errors['profile_picture_error'] = "This image is not valid."
        if not years_of_experience == None:
            years_of_experience = self.json_to_int(years_of_experience)
            if years_of_experience:
                fields_to_update['years_of_experience'] = years_of_experience
            else:
                errors['years_of_experience_error'] = "This property needs to be an integer."

        return fields_to_update, errors
