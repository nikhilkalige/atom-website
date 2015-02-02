var AmpersandView = require("ampersand-view");
var PackageModel = require("../models/package");
var Template = require("./templates/package.hbs");
var Graphs = require("./graph_view.js");


module.exports = AmpersandView.extend({
    template: Template,
    subviews: {
        g: {
            container: "#metric",
            prepareView: function(el) {
                return new Graphs({
                    el: el,
                    data: this.model.downloads_list
                });
            }
        }
    },
    render: function() {
        this.renderWithTemplate();
    },
    bindings: {
        "model.name": {
            type: "text",
            hook: "name"
        },
        "model.description": {
            type: "text",
            hook: "desc"
        },
        "model.version.number": {
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
        },
        "model.stars": {
            type: "text",
            hook: "stars"
        }
    },
    initialize: function(options) {
        self = this;
        this.title = captialize(options.name);
        this.model = new PackageModel();
        this.model.on("change", function() {
            app.router.trigger("page", self);
        })
        this.model.on("error", function() {
            app.router.trigger("error4");
        })
        this.model.fetch_model(options.name);
    }
});

var captialize = function(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
