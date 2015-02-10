
var IndexView = require("../components/index/js/index-view.js");
var ComponentTwoView = require("../components/component-two/js/component-two-view.js");
var ComponentThreeView = require("../components/component-three/js/component-three-view.js");

module.exports = (function() {
    'use strict';

    return {
        startIndex: function() {
            var indexView = new IndexView();
        },

        startComponentOne: function() {
            require.ensure([], function() {
                var ComponentOneView = require("../components/component-one/js/component-one-view.js");
                var componentOneView = new ComponentOneView();
            });
        },

        startComponentTwo: function() {
            var componentTwoView = new ComponentTwoView();
        },

        startComponentThree: function() {
            var componentThreeView = new ComponentThreeView();
        }
    }
    
})();


