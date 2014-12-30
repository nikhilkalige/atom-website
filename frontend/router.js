var Router = require('ampersand-router');

module.exports = Router.extend({
    routes: {
        "": "index",
        "package/:name": "packages",
        ":name": "name_route"
    },
    index: function() {
    },
    name_route: function(name) {
        this.redirectTo("package/" + name);
    },
    packages: function(name) {
    },
    setFilter: function (arg) {
        app.me.mode = arg || 'all';
    }
});
