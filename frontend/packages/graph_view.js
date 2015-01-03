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
            title: "UFO Sightings",
            description: "Yearly UFO sightings from 1945 to 2010.",
            data: this.model.downloads,
            width: 650,
            height: 250,
            target: this.el,
            show_years: false,
            animate_on_load: true,
            x_accessor: "date",
            y_accessor: "count",
            interpolate: "monotone"
        });
        console.log("meee");
    }
});
