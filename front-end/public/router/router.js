
var Backbone = require("backbone");
var componentManager = require("../component-manager/component-manager.js");

var router = (function() {
    
    'use strict';

    return {
        start: function() {
            var AppRouter = Backbone.Router.extend({
                routes: {
                    "": "index",
                    "component-one": "componentOne",
                    "component-two": "componentTwo",
                    "component-three": "componentThree",
                    "*actions": "error" 
                },

                index: function() {
                    componentManager.startIndex();
                },

                componentOne: function() {
                    componentManager.startComponentOne();
                },

                componentTwo: function() {
                    componentManager.startComponentTwo();
                },

                componentThree: function() {
                    componentManager.startComponentThree();
                },

                error: function() {
                    console.log("ERROR");
                }
            }); 

            var appRouter = new AppRouter();

            Backbone.history.start();
        }
    }
})();

module.exports = router;
