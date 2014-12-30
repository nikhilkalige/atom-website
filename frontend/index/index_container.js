var AmpersandView = require("ampersand-view");
var Template = require("./templates/index.hbs");
var StatsView = require("./stats_view");
var FeatureView = require("./feature_view");
var StatsModel = require("../models/stats");
var PackageModel = require("../models/package")
var FeatureCollection = require("../models/featured")

module.exports = AmpersandView.extend({
    template: Template,
    events: {},
    subviews: {
        stats: {
            container: '[data-hook=stats]',
            prepareView: function(el) {
                return new StatsView({
                    el: el,
                    model: this.stats_model
                });
            }
        },
    },
    initialize: function() {
        self = this;
        this.stats_model = new StatsModel();
        app.features = new FeatureCollection();
        app.router.on("route:index", function(a, b) {
            console.log("route init");
            self.render();
        });
        app.features.on("reset", function() {
            console.log("resetttasdf");
            self.renderCollection(app.features, FeatureView, self.queryByHook("featured"));
        })
        app.router.on("route:package", function(a, b) {
            console.log(a, b);
        })

        this.stats_model.fetch();
        app.features.fetch({reset: true});
    }
});
