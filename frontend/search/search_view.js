var AmpersandView = require("ampersand-view");
var SearchCollection = require("./search_model");
var PackageTemplate = require("../templates/package-widget.hbs");
var SearchTemplate = require("./templates/search_view.hbs");

module.exports = AmpersandView.extend({
    template: SearchTemplate,
    initialize: function(options) {
        this.coll = new SearchCollection();
        this.coll.search(options.param);
    },
    render: function() {
        var self = this;
        this.coll.once("reset", function() {
            self.renderCollection(this.coll, PackageTemplate, self.queryByHook("widgets"));
        });
        this.renderWithTemplate();
    }
});
