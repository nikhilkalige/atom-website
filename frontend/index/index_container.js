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
                    model: this.stats
                });
            }
        },
    },
    initialize: function() {
        self = this;
        this.stats = new StatsModel();
        app.router.on("route:index", function(a, b) {
            console.log("route init");

            features = new FeatureCollection();
            self.stats.fetch();
            features.fetch({reset: true});

            features.once("reset", function() {
                console.log("resetttasdf");
                self.renderCollection(features, FeatureView, self.queryByHook("featured"));
            })
            self.render();
        });

        app.router.on("route:package", function(a, b) {
            console.log(a, b);
        })

    }
});
