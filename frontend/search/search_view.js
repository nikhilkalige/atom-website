var AmpersandView = require("ampersand-view");
var SearchCollection = require("./search_model");
var PackageTemplate = require("../index/templates/feature.hbs");
var SearchTemplate = require("./templates/search_view.hbs");
var ItemView = require("../index/feature_view");

module.exports = AmpersandView.extend({
    template: SearchTemplate,
    props: {
        query_string: 'string'
    },
    bindings: {
        "collection.results": {
            type: function(el, value, previous) {
                var str;
                if(value === 0) {
                    str = "Sorry, no result"
                }
                else if(value == 1){
                    str = value + " result";
                }
                else {
                    str = value + " results";
                }

                str+= ' for <a href="/search/' +
                    this.query_string + '&page=1">&lsquo;' + this.query_string+
                    '&rsquo;</a>';

                el.innerHTML = str;
            },
            hook: "results"
        }
    },
    initialize: function(options) {
        this.query_string = options.param;
        this.collection = new SearchCollection();
        this.collection.search(this.query_string);
    },
    render: function() {
        var self = this;
        this.collection.once("reset", function() {
            self.renderCollection(self.collection, ItemView, self.queryByHook("widgets"));
            self.trigger('change:collection.pages');
            self.trigger('change:collection.results');
        });
        this.renderWithTemplate();
    }
});
