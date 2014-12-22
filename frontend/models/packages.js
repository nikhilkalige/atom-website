var AmpersandCollection = require('ampersand-rest-collection');
var Package = require('./package');

module.exports = AmpersandCollection.extend({
    model: Package,
    url: '/api/package'
});
