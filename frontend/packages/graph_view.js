$ = jQuery = require("jquery");
d3 = require("d3");
var MetricsGraphs = require("metrics-graphics");
var AmpersandView = require("ampersand-view");
var DownloadsModel = require("../models/downloads");

module.exports = AmpersandView.extend({
    template: "",
    initialize: function(options) {
        this.model = new DownloadsModel({
            downloads: options.data
        }, {parse:true});
    },
    render: function() {
        MetricsGraphs.convert.date(this.model.downloads, 'date');
        MetricsGraphs.data_graphic({
            data: this.model.downloads,
            width: 760,
            height: 250,
            target: this.el,
            show_years: false,
            animate_on_load: true,
            x_accessor: "date",
            y_accessor: "count",
            // Axis related
            min_y_from_data: true,
            min_x_from_data: true,
            concise: false,
            // Layout related
            buffer: 5,
            // Graphic
            interpolate: "linear",
            point_size: 4,
            y_rug: true
        });
    }
});
