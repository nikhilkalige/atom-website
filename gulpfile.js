/**
 * uses browserify and minifies code in production build
 */

var scripts = function(options) {
    var settings = _.extend({
        watching: false,
        which: 'index.coffee'
    }, options);


