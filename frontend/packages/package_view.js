var AmpersandView = require("ampersand-view");
var PackageModel = require("../models/package");
var Template = require("./templates/package.hbs");

module.exports = AmpersandView.extend({
    template: Template,
});
