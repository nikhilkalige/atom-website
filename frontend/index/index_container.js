var AmpersandView = require("ampersand-view");
var Template = require("./templates/index.hbs");
var StatsView = require("./stats_view");
var FeatureView = require("./feature_view");
var StatsModel = require("../models/stats")
//var FeatureCollection = require("../models/featured")

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
  /*      featured: {
            container: "[data-hook=featured]",
            prepareView: function(el) {
                this.renderCollection(app.features, FeatureView, this.queryByHook("featured"))
            }
        }
  */  },
    initialize: function() {
        self = this;
        this.stats_model = new StatsModel();
        //app.features = new FeatureCollection();
        this.stats_model.fetch();
        //app.features.fetch();
        app.router.on("route:index", function(a, b) {
            console.log("route init");
            self.render();
        });
    }
});
