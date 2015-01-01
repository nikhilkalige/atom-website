var AmpersandModel = require("ampersand-model");

module.exports = AmpersandModel.extend({
    props: {
        count: ["string", true, "0"],
        day: ["string", true, "0"],
        month: ["string", true, "0"],
        week: ["string", true, "0"],
    },
    parse: function(res) {
        res.count = this.prettify(res.count);
        res.day = this.prettify(res.day);
        res.month = this.prettify(res.month);
        res.week = this.prettify(res.week);
        return res;
    },
    prettify: function(number) {
        var parts = number.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        return parts.join(".");
    },
    urlRoot: "api/packages/stats"
})

