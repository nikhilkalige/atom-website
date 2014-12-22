var Router = require('ampersand-router');

module.exports = Router.extend({
    routes: {
        "": "index"
    },
    index: function() {
        console.log("index page");
    },
    setFilter: function (arg) {
        app.me.mode = arg || 'all';
    }
});
