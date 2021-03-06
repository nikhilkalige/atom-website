var AmpersandView = require("ampersand-view");
var Template = require("./templates/stats.hbs");
var Model = require("../models/stats")

module.exports = AmpersandView.extend({
    template: Template,
    bindings: {
        "model.count": "[data-hook~=count]",
        "model.day": "[data-hook~=day]",
        "model.month": "[data-hook~=month]",
        "model.week": "[data-hook~=week]",
    },
    render: function() {
        this.renderWithTemplate();
    }
})
