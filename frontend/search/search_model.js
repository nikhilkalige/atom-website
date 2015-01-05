var AmpersandCollection = require('ampersand-rest-collection');
var Package = require('../models/package');

module.exports = AmpersandCollection.extend({
    model: Package,
    param: "",
    url: function() {
        return ('/api/package?q={"filters":[' +
            '{"name": "name", "val": "%' + this.param + '%", "op": "like"},' +
            '{"name": "keywords__name", "val":"' + this.param + '", "op": "any"}' +
            '],"disjunction":true}');
    },
    parse: function(res, options) {
        return res.results;
    },
    search: function(param) {
        this.param = param;
        this.fetch();
    }
});

    /*num_results: 0,
    num_pages: 0,
*/
