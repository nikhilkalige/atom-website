var Router = require("./router");
//var Switcher = require("./switcher");
var MainView = require("./main/main_view");

window.app = {
    init: function() {
        this.router = new Router();
        //Switcher(this.queryByHook("container"));
        new MainView({});
        this.router.history.start({pushState: true});
    }
};

window.app.init();
