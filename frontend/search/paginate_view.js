var AmpersandView = require("ampersand-view");
var Template = require("./templates/paginate.hbs");


module.exports = AmpersandView.extend({
    template: Template,
    props: {
        pages: ["number", true, 0],
        url: ["string", true, ""]
    },
    derived: {
        previous: {
            dep: ["active"],
            fn: function() {
                if(this.active != 1)
                    return this.active - 1;
                else
                    return null;
            }
        },
        next: {
            deps: ["active", "pages"],
            fn: function() {
                if(this.active < this.pages)
                    return this.active + 1;
                else
                    return null;
            }
        },
        prev_url: {
            deps: ["previous"],
            fn: function() {
                if(this.previous)
                    return this.url + this.previous;
            }
        },
        next_url: {
            deps: ["next"],
            fn: function() {
                if(this.next)
                    return this.url + this.next;
            }
        },
        active_url: {
            deps: ["active"],
            fn: function() {
                return this.url + this.active;
            }
        }
    },
    bindings: {
        "active": {
            type: "text",
            hook: "active"
        },
        "prev_url": {
            type: "attribute",
            name: "href",
            hook: "prev"
        },
        "next_url": {
            type: "attribute",
            name: "href",
            hook: "next"
        },
        "active_url": {
            type: "attribute",
            name: "href",
            hook: "active"
        }
    },
    session: {
        active: ["number", true, 1]
    },
    initialize: function(options) {
        this.pages = options.pages;
        this.url = "/" + app.router.history.getPath().split('&')[0] + "&page=";
        this.active = options.current_page;
    }
});
