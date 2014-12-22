var Router = require("./router");
var IndexView = require("./index/index_container");

window.app = {
    init: function() {
        this.router = new Router();
        new IndexView({
            el: document.querySelector("body>div")
        });
        this.router.history.start();

    }

};

window.app.init();
