var browserify = require("browserify");
var watchify = require("watchify");
var source = require("vinyl-source-stream");
var buffer = require("vinyl-buffer");
var _ = require("underscore");
var gulp = require("gulp");
var gutil = require('gulp-util');
var plugins = require('gulp-load-plugins')();

var paths = {
    "scripts_dst": "public/js"
}

var onError = function(error) {
    gutil.log(gutil.colors.red(error));
};

/**
 * uses browserify and minifies code in production build
 */
var scripts = function(options) {
    var settings = _.extend({
        name: "",
        source: "",
        watching: false,
        deps: [],
        require: []
    }, options);

    var bundler = browserify(settings.source, {
        debug: true,
        extensions: [".js", ".hbs", '.jade']
    });

    bundler.transform("hbsfy");
    bundler.transform("jadeify");

    if(settings.watching)
        bundler = watchify(bundler);

    if(settings.deps.length > 0)
        bundler.external(deps);

    if(settings.require.length > 0)
        bundler.require(deps);

    var rebundle = function() {
        return bundler.bundle()
            .on("error", onError)
            .pipe(source(settings.name))
            .pipe(buffer())
            .pipe(gulp.dest(paths.scripts_dst));
    };

    bundler.on("update", rebundle);
    bundler.on("log", function(msg) {
        gutil.log(gutil.colors.green(msg))
    });
    return rebundle();
};

var deps = [
    "ampersand-collection",
    "ampersand-router",
    "ampersand-state",
    "ampersand-subcollection",
    "ampersand-view"
];

/**
 * build all vendor files
 */
gulp.task("scripts-vendors", function() {
    return scripts({
        name: "vendors.js",
        require: deps
    });
});

gulp.task("scripts-watch-vendors", function() {
    return scripts({
        name: "vendors.js",
        require: deps,
        watching: true
    });
});

/**
 * build all client files
 */
gulp.task("scripts-client", function() {
    return scripts({
        name: "app.js",
        source: "./frontend/app.js",
        deps: deps
    });
});

gulp.task("scripts-watch-client", function() {
    return scripts({
        name: "app.js",
        source: "./frontend/app.js",
        watching: true,
        deps: deps
    });
});

/**
 * combine vendors and clients into single build for production
 */
gulp.task('concat-scripts', function() {
    var src = [
        path.join(path.scripts_dst, 'vendors.js'),
        path.join(path.scripts_dst, 'app.js')
    ];
    return gulp.src(src)
        .pipe(plugins.concat('build.min.js'))
        .pipe(plugins.size({ showFiles: true }))
        .pipe(gulp.dest(path.scripts_dst));
});

/**
 * build all javascript files
 */
gulp.task("build-js", ["scripts-vendors", "scripts-client"]);
gulp.task("build-watch-js", ["scripts-vendors", "scripts-watch-client"]);

gulp.task("default", ["build-watch-js"]);
