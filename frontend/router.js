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
    initialize: function() {
        //this.bind('route', this.track_page);
    },
    index: function() {
        this.trigger("page", new IndexView({}));
    },
    name_route: function(name) {
        //console.log(name);
        this.redirectTo("package/" + name);
    },
    packages: function(name) {
        //this.trigger("page", new PackageView({name: name}));
        new PackageView({name: name});
    },
    search: function(param) {
        name = param.split('&')[0];
        no = param.split('&')[1]
        if(no != null)
            no = no.split("page=")[1]

        new SearchView({name: name, page_no: no});
    },
    track_page: function() {
        ga('send', 'pageview', {
            page: "/" + this.history.getFragment()
        });
    },
    setFilter: function (arg) {
        app.me.mode = arg || 'all';
    }
});
