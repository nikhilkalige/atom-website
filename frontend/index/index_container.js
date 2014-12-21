var AmpersandView = require("ampersand-view");
var Container = require("./templates/index.hbs");

module.exports = AmpersandView.extend({
    template: Container,
    events: {},
    autoRender: true,
    initialize: function() {
        app.router.on("route:index", function() {
            console.log("route init");
        });
    }
});
