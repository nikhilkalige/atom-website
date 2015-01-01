var AmpersandModel = require("ampersand-model");
var Moment = require("moment");

module.exports = AmpersandModel.extend({
    props: {
        id: "any",
        name: ["string", true, ""],
        author: ["string", true, ""],
        url: ["string", true, ""],
        description: ["string", true, ""],
        stars: ["number", true, 0],
        downloads: ["object", true],
        downloads_list: ["array", true],
        keywords: ["array", true],
        license: ["object", true],
        version: ["object", true],
        dependencies: ["object", true]
    },
    derived: {
        "last_published": {
            deps: ["version"],
            fn: function() {
                return Moment(this.version.date).fromNow();
            }
        }
    },
    urlRoot: "api/packages"
})

