var AmpersandView = require("ampersand-view");
var AmpersandViewSwitcher = require('ampersand-view-switcher');
var PackageModel = require("../models/package");
var Template = require("./templates/index_search.hbs");
var ErrorView = require("../error/error_404_view");

module.exports = AmpersandView.extend({
    template: Template,
    events: {
        "submit form": "search"
    },
    initialize: function() {
        var self = this;
        app.router.once("page", function() {
            self.el = document.querySelector("body>div");
            self.render();
        })
        this.listenTo(app.router, "page", this.page_switcher);
        this.listenTo(app.router, "error4", this.error_switcher);

    },
    render: function() {
        this.renderWithTemplate({});
        this.switcher = new AmpersandViewSwitcher(this.queryByHook("contents"), {
            show: function(newView, oldView) {
                app.currentPage = newView;
            }
        });
    },
    error_switcher: function() {
        app.router.trigger("page");
        this.page_switcher(new ErrorView({}));
    },
    page_switcher: function(view) {
        //console.log("switcher");
        if(view != null)
            this.switcher.set(view);
    },
    search: function(event) {
        event.preventDefault();
        value = this.query("#site-search").value;
        //console.log("search:"+ encodeURIComponent(value) )
        if(value != "") {
            // query the server for data
            app.router.redirectTo("search/" + encodeURIComponent(value));
        }
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
