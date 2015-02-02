var AmpersandView = require("ampersand-view");
var SearchCollection = require("./search_model");
var PackageTemplate = require("../index/templates/feature.hbs");
var SearchTemplate = require("./templates/search_view.hbs");
var ItemView = require("../index/feature_view");
var PaginateView = require("./paginate_view");

module.exports = AmpersandView.extend({
    template: SearchTemplate,
    props: {
        query_string: 'string',
    },
    derived: {
        title: {
            deps: ['query_string'],
            fn: function() {
                return "Results for " + this.query_string;
            }
        }
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
        var self = this;
        this.query_string = options.name;
        this.collection = new SearchCollection();
        this.collection.search(this.query_string, options.page_no);
        this.collection.once("reset", function() {
            self.trigger('change:collection.pages');
            self.trigger('change:collection.results');
            app.router.trigger("page", self);
        });
        this.collection.on("error", function() {
            app.router.trigger("error4");
        })
    },
    render: function() {
        this.renderWithTemplate();
        this.renderCollection(this.collection, ItemView, this.queryByHook("widgets"));
        if(this.collection.pages > 1) {
            this.renderSubview(new PaginateView({
                pages: this.collection.pages,
                current_page: this.collection.current_page
            }),
            this.queryByHook('paginate'));
        }
    }
});
