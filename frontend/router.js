var Router = require('ampersand-router');
var IndexView = require("./index/index_container");
var PackageView = require("./packages/package_view");
var SearchView = require("./search/search_view");

module.exports = Router.extend({
    routes: {
        "": "index",
        "package/:name": "packages",
        //search?q=asdf
        "search/:param": "search",
        ":name": "name_route"
    },
    index: function() {
        this.trigger("page", new IndexView({}));
    },
    name_route: function(name) {
        console.log(name);
        this.redirectTo("package/" + name);
    },
    packages: function(name) {
        this.trigger("page", new PackageView({}));
    },
    search: function(param) {
        this.trigger("page", new SearchView({param: param}));
    },
    setFilter: function (arg) {
        app.me.mode = arg || 'all';
    }
});
