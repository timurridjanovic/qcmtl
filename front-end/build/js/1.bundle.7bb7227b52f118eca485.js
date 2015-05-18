webpackJsonp([1],{

/***/ 8:
/***/ function(module, exports, __webpack_require__) {

	
	var template = __webpack_require__(13);
	var Backbone = __webpack_require__(4);
	var $ = __webpack_require__(2);
	__webpack_require__(20);

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


/***/ },

/***/ 13:
/***/ function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(24);
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "\n<h1>Welcome to component one</h1>\n\n<a href=\"#\">Go back to index page</a>\n";
	  },"useData":true});

/***/ },

/***/ 20:
/***/ function(module, exports, __webpack_require__) {

	// style-loader: Adds some css to the DOM by adding a <style> tag

	// load the styles
	var content = __webpack_require__(21);
	if(typeof content === 'string') content = [[module.id, content, '']];
	// add the styles to the DOM
	var update = __webpack_require__(22)(content, {});
	// Hot Module Replacement
	if(false) {
		// When the styles change, update the <style> tags
		module.hot.accept("!!/Users/tridjanovic/Documents/google-app-engine-projects/qcmtl/front-end/node_modules/css-loader/index.js!/Users/tridjanovic/Documents/google-app-engine-projects/qcmtl/front-end/node_modules/sass-loader/index.js!/Users/tridjanovic/Documents/google-app-engine-projects/qcmtl/front-end/public/components/component-one/scss/component-one.scss", function() {
			var newContent = require("!!/Users/tridjanovic/Documents/google-app-engine-projects/qcmtl/front-end/node_modules/css-loader/index.js!/Users/tridjanovic/Documents/google-app-engine-projects/qcmtl/front-end/node_modules/sass-loader/index.js!/Users/tridjanovic/Documents/google-app-engine-projects/qcmtl/front-end/public/components/component-one/scss/component-one.scss");
			if(typeof newContent === 'string') newContent = [[module.id, newContent, '']];
			update(newContent);
		});
		// When the module is disposed, remove the <style> tags
		module.hot.dispose(function() { update(); });
	}

/***/ },

/***/ 21:
/***/ function(module, exports, __webpack_require__) {

	exports = module.exports = __webpack_require__(23)();
	exports.push([module.id, ".w-component-one{width:980px;margin:0 auto;margin-top:20px;text-align:center}.w-component-one h1{color:red}", ""]);

/***/ }

});