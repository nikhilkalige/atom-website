var AmpersandCollection = require('ampersand-rest-collection');
var Package = require('../models/package');

module.exports = AmpersandCollection.extend({
    model: Package,
    pages: 0,
    current_page: 0,
    results: 0,
    param: "",
    url: function() {
        var url = '/api/search?q={"name": "' + this.param + '"}';
        if(isNaN(this.page_no) == false)
            url = url + "&page=" + this.page_no;

        return url;
    },
    parse: function(res, options) {
        this.pages = res.total_pages;
        this.current_page = res.page;
        this.results = res.num_results;
        return res.objects;
    },
    search: function(param, page_no) {
        this.param = param;
        this.page_no = page_no;
        this.fetch({reset: true});
    }
});

