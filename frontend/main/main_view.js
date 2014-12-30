var AmpersandView = require("ampersand-view");
var AmpersandViewSwitcher = require('ampersand-view-switcher');
var PackageModel = require("../models/package");
var Template = require("./templates/index_search.hbs");

module.exports = AmpersandView.extend({
    template: Template,
    initialize: function() {
        var self = this;
        app.router.once("page", function() {
            self.el = document.querySelector("body>div");
            self.render();
        })
        this.listenTo(app.router, "page", this.page_switcher);

    },
    render: function() {
        this.renderWithTemplate({});
        this.switcher = new AmpersandViewSwitcher(this.queryByHook("contents"), {
            show: function(newView, oldView) {
                app.currentPage = newView;
            }
        });
    },
    page_switcher: function(view) {
        console.log("switcher");
        if(view != null)
            this.switcher.set(view);
    }
});

/*
var AmpersandViewSwitcher = require('ampersand-view-switcher');

var switcher = null;

var page_handler = function(view) {
    switcher.set(view)
};

module.exports = function(container_hook) {
    switcher =  new AmpersandViewSwitcher(container_hook, {
        show: function(newView, oldView) {
            app.currentPage = newView;
        }
    });
    app.router.on("page", page_handler);
};*/
