
var template = require("../hbs/component-two.hbs");
var Backbone = require("backbone");
var $ = require("jquery");
require("../scss/component-two.scss");

module.exports = (function() {
    'use strict';

    var ComponentTwoView = Backbone.View.extend({
        template: template,

        className: "w-component-two",

        initialize: function() {
            this.render();
        },

        render: function() {
            this.$el.html(this.template());
            $(".app").empty().html(this.$el);
        }
    });

    return ComponentTwoView;
    
})();
