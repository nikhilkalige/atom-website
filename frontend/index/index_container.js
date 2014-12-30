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
    render: function() {
        features = new FeatureCollection();
        self.stats.fetch();
        features.fetch({reset: true});

        features.once("reset", function() {
            self.renderCollection(features, FeatureView, self.queryByHook("featured"));
        })
        this.renderWithTemplate();
    },
    initialize: function() {
        self = this;
        this.stats = new StatsModel();
    }
});
