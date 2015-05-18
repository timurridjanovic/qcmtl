var $ = require('jquery');
var url = 'http://localhost:8080/api/v1/users';

var runUserTests = function() {
    //creating a user in database
    describe('Creating a user in the database', function() {
        var value;
        var ajaxMethod = jasmine.createSpy('user creation POST request');
        var user = {
            email: "timmy@gmail.com",
            password: "12345678",
            first_name: "timmy",
            last_name: "ridji",
            phone_number: "658-9999",
            city: "Montreal",
            sex: "Male",
            province: "Quebec",
            country: "Canada",
            date_of_birth: new Date('06/21/1985').getTime()
        };

        beforeAll(function(done) {
            $.post(url, user).done(function(data) {
                value = data;
                ajaxMethod();
                done();
            });
        });

        it("user post request received", function(done) {
            expect(ajaxMethod).toHaveBeenCalled();
            done();
        });

        it("user creation validation", function(done) {
            console.log("MAN");
            console.log(JSON.stringify(value));
            expect(value.users[0].province).toEqual(user.province);
            expect(value.users[0].email).toEqual(user.email);
            expect(value.users[0].first_name).toEqual(user.first_name);
            expect(value.users[0].last_name).toEqual(user.last_name);
            expect(value.users[0].city).toEqual(user.city);
            expect(value.users[0].country).toEqual(user.country);
            expect(value.users[0].sex).toEqual(user.sex);
            expect(value.users[0].phone_number).toEqual(user.phone_number);
            done();
        });
    });

    describe("Testing users get request", function() {
        var originalTimeout;
        var value;
        var ajaxMethod = jasmine.createSpy('users get request');

        beforeAll(function(done) {
            originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
            jasmine.DEFAULT_TIMEOUT_INTERVAL = 30000;
            $.ajax({
                url: 'http://localhost:8080/api/v1/users',
                type: 'GET',
                success: function(data) {
                    value = data;
                    ajaxMethod();
                    done();
                }
            });
        });
        
        it("users get request received", function(done) {
            var email = value.users[0].email;
            expect(ajaxMethod).toHaveBeenCalled();
            done();
        });

        it("first users email is valid", function(done) {
            var email = value.users[0].email;
            expect(email).toEqual('timur@gmail.com');
            done();
        });

        afterAll(function(done) {
            jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
            done();
        });
    });
};

module.exports = runUserTests;
