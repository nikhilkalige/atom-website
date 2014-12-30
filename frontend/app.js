var Router = require("./router");
var Switcher = require("./switcher");

window.app = {
    init: function() {
        this.router = new Router();
        Switcher(document.querySelector("container"));

        this.router.history.start({pushState: true});
    }
};

window.app.init();
