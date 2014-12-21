var AmpersandModel = require("ampersand-model");

module.exports = AmpersandModel.extend({
    props: {
        id: "any",
        name: ["string", true, ""],
        author: ["string", true, ""],
        link: ["string", true, ""],
        description: ["string", true, ""],
        downloads: ["number", true, 0]
    }
})

