var Router = require('ampersand-router');
var IndexView = require("./index/index_container");
var PackageView = require("./packages/package_view");

module.exports = Router.extend({
    routes: {
        "": "index",
        "package/:name": "packages",
        ":name": "name_route"
    },
    index: function() {
        this.trigger("page", new IndexView({}));
    },
    name_route: function(name) {
        this.redirectTo("package/" + name);
    },
    packages: function(name) {
        this.trigger("page", new PackageView({}));
    },
    setFilter: function (arg) {
        app.me.mode = arg || 'all';
    }
});
