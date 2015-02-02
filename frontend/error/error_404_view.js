var AmpersandView = require("ampersand-view");
var Template = require("./templates/error_404.hbs");


module.exports = AmpersandView.extend({
    template: Template,
    title: "Atom"
});
