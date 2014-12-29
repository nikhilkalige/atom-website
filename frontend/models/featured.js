var AmpersandCollection = require('ampersand-rest-collection');
var Package = require('./package');

module.exports = AmpersandCollection.extend({
    model: Package,
    url: 'http://localhost:5000/api/package'
});

