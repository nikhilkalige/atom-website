var AmpersandViewSwitcher = require('ampersand-view-switcher');

var switcher = null;

var page_handler = function(view) {
    switcher.set(view)
};

module.exports = function(container_hook) {
    switcher =  new AmpersandViewSwitcher(this.queryByHook(container_hook), {
        show: function(newView, oldView) {
            app.currentPage = newView;
        }
    });
    app.router.on("page", page_handler);
};
