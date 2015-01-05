var AmpersandModel = require("ampersand-model");
var Moment = require("moment");

module.exports = AmpersandModel.extend({
    idAttribute: "name",
    attributeId: "name",
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
        readme: ["string", true, ""],
        issues: ["object", true],
        pull: ["object", true],
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
    urlRoot: function() {
        return "/api/package";
    },
    fetch_model: function(name) {
        var url = this.urlRoot() + '/' + name
        this.fetch({url: url});
    },
    parse: function(res) {
        res.downloads.total = this.prettify(res.downloads.total);
        res.downloads.day = this.prettify(res.downloads.day);
        res.downloads.month = this.prettify(res.downloads.month);
        res.downloads.week = this.prettify(res.downloads.week);
        return res;
    },
    prettify: function(number) {
        var parts = number.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        return parts.join(".");
    }
})

