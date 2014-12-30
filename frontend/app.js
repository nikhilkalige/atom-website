var Router = require("./router");
var IndexView = require("./index/index_container");
var PackageView = require("./packages/package_view");

window.app = {
    init: function() {
        this.router = new Router();
        new IndexView({
            el: document.querySelector("body>div")
        });
        //new IndexView();
        this.router.history.start({pushState: true});

    }

};

window.app.init();
