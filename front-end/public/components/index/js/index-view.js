
var template = require("../hbs/index.hbs");
var Backbone = require("backbone");
var $ = require("jquery");
require("../scss/index.scss");

module.exports = (function() {
    'use strict';

    var IndexView = Backbone.View.extend({
        template: template,

        tagName: "div",

        className: "w-index",

        initialize: function() {
            this.render();
        },

        render: function() {
            this.$el.html(this.template());
            $(".app").empty().html(this.$el);
        }
    });

    return IndexView;
    
})();
