var AmpersandCollection = require('ampersand-rest-collection');
var Package = require('../models/package');

module.exports = AmpersandCollection.extend({
    model: Package,
    pages: 0,
    current_page: 0,
    results: 0,
    param: "",
    url: function() {
        return ('/api/search?q={"name": "' + this.param + '"}');
    },
    parse: function(res, options) {
        this.pages = res.total_pages;
        this.current_page = res.page;
        this.results = res.num_results;
        return res.objects;
    },
    search: function(param) {
        this.param = param;
        this.fetch({reset: true});
    }
});

