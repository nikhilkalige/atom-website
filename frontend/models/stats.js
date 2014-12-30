var AmpersandModel = require("ampersand-model");

module.exports = AmpersandModel.extend({
    props: {
        count: ["number", true, 0],
        day: ["number", true, 0],
        month: ["number", true, 0],
        week: ["number", true, 0],
    },
    urlRoot: "api/packages/stats"
})

