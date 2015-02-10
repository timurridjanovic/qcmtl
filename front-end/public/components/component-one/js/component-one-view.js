
var template = require("../hbs/component-one.hbs");
var Backbone = require("backbone");
var $ = require("jquery");
require("../scss/component-one.scss");

module.exports = (function() {
    'use strict';

    var ComponentOneView = Backbone.View.extend({
        template: template,

        className: "w-component-one",

        initialize: function() {
            this.render();
        },

        render: function() {
            this.$el.html(this.template());
            $(".app").empty().html(this.$el);
        }
    });

    return ComponentOneView;
    
})();
