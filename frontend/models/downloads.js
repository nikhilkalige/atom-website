var AmpersandState = require("ampersand-state");
var Moment = require("moment");

module.exports = AmpersandState.extend({
    props:  {
        downloads: ["object", true]
    },
    parse: function(data) {
        var results = [];
        var obj = {};

        today = Moment();
        for(var i = 0; i < data.downloads.length; i++) {
            var d = today.subtract(1, 'd').format('YYYY-MM-DD');
            if(i == 0)
                d = today.format('YYYY-MM-DD');
            obj = {
                date: d,
                count: data.downloads[i]
            }
            results.push(obj);
        }
        data.downloads = results;
        return data;
    }
});
