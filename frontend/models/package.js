var AmpersandModel = require("ampersand-model");

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
    urlRoot: "api/packages"
})

