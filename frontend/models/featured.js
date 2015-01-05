var AmpersandCollection = require('ampersand-rest-collection');
var Package = require('./package');

module.exports = AmpersandCollection.extend({
    model: Package,
    url: '/api/packages/featured',
    parse: function(res, options) {
        return res.results;
    }
});

