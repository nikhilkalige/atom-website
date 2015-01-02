var AmpersandView = require("ampersand-view");
var PackageModel = require("../models/package");
var Template = require("./templates/package.hbs");

module.exports = AmpersandView.extend({
    template: Template,
    bindings: {
        "model.name": {
            type: "text",
            hook: "name"
        },
        "model.description": {
            type: "text",
            hook: "desc"
        },
        "model.version.name": {
            type: "text",
            hook: "ver"
        },
        "model.author": {
            type: "text",
            hook: "author"
        },
        "model.url": [
            {
                type: "text",
                hook: "url"
            },
            {
                type: "attribute",
                hook: "url",
                name: "href"
            }
        ],
        "model.license.name": {
            type: "text",
            hook: "license"
        },
        "model.license.url": {
            type: "attribute",
            hook: "license",
            name: "href"
        },
        "model.downloads.day": {
            type: "text",
            hook: "day"
        },
        "model.downloads.month": {
            type: "text",
            hook: "month"
        },
        "model.downloads.week": {
            type: "text",
            hook: "week"
        }


    },
    initialize: function(options) {
        self = this;
        this.model = new PackageModel();
        this.model.on("change", function() {
            app.router.trigger("page", self);
        })
        this.model.fetch_model(options.name);
    }
});
