var AmpersandView = require("ampersand-view");
var Template = require("./templates/feature.hbs");


module.exports = AmpersandView.extend({
    template: Template,
    bindings: {
        "model.name": [
            {
                type: "text",
                hook: "link",
            },
            {
                type: "attribute",
                hook: "link",
                name: "href"
            },
            {
                type: "attribute",
                hook: "version",
                name: "href"
            },
            {
                type: "attribute",
                hook: "author",
                name: "href"
            }

        ],
        "model.description": {
            type: "text",
            selector: ".description",
        },
        "model.version.number": {
            type: "text",
            hook: "version",
        },
        "model.author": {
            type: "text",
            hook: "author",
        }
        /*"model.description": {
            type: "text",
            selector: ".quiet",
        },*/
    }
})
