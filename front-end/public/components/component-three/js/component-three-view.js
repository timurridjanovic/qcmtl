

var template = require("../hbs/component-three.hbs");
var Backbone = require("backbone");
var $ = require("jquery");
require("../scss/component-three.scss");

module.exports = (function() {
    'use strict';

    var ComponentThreeView = Backbone.View.extend({
        template: template,

        className: "w-component-three",

        initialize: function() {
            this.render();
        },

        render: function() {
            this.$el.html(this.template());
            $(".app").empty().html(this.$el);
        }
    });

    return ComponentThreeView;
    
})();
