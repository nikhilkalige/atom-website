var browserify = require("browserify");
var watchify = require("watchify");
var source = require("vinyl-source-stream");
var buffer = require("vinyl-buffer");
var _ = require("underscore");
var gulp = require("gulp");
var gutil = require('gulp-util');
var nib = require('nib');
var stylus = require('gulp-stylus');
var plugins = require('gulp-load-plugins')();
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var git = require('gulp-git');
var path = require('path');
var size = require('gulp-size');
var sequence = require('gulp-sequence');
var minify_css = require('gulp-minify-css');
var rename = require("gulp-rename");
var htmlreplace = require('gulp-html-replace');

var paths = {
    //"scripts_dst": "public/js"
    "scripts_dst": "app/static/js",
    "css_dst": "app/static/css",
    "css_src": "frontend/static/css/index.styl",
    "html": "app/templates/index.html",
    "prod_js": "app/static/js/index.min.js",
    "prod_css": "app/static/css/index.min.css",
    "full_js": "app/static/js/app.full.js",
}

var onError = function(error) {
    gutil.log(gutil.colors.red(error));
};

/**
 * Build all css files
 */
gulp.task('css', function () {
    return gulp.src(paths.css_src)
        .pipe(stylus({use: [nib()]}))
        .pipe(gulp.dest(paths.css_dst));
});

gulp.task('css-minify', function () {
    return gulp.src(path.join(paths.css_dst, 'index.css'))
        .pipe(minify_css())
        .pipe(rename('index.min.css'))
        .pipe(gulp.dest(paths.css_dst));
});

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
        extensions: [".js", ".hbs"]
    });

    bundler.transform("hbsfy");

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
    "ampersand-model",
    "ampersand-rest-collection",
    "ampersand-router",
    "ampersand-state",
    "ampersand-subcollection",
    "ampersand-view",
    "ampersand-view-switcher",
    "d3",
    "jquery",
    "metrics-graphics",
    "moment"
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

gulp.task("scripts-production", function() {
    return scripts({
        name: "app.full.js",
        source: "./frontend/app.js",
    });
});

/**
 * combine vendors and clients into single build for production
 */
gulp.task('js-minify', function() {
    return gulp.src(paths.full_js)
        .pipe(size({ showFiles: true }))
        .pipe(uglify())
        .pipe(rename('index.min.js'))
        .pipe(gulp.dest(paths.scripts_dst));
});

/**
 * build all javascript files
 */
gulp.task("build-js", ["scripts-vendors", "scripts-client"]);
gulp.task("build-watch-js", ["scripts-vendors", "scripts-watch-client"]);

/**
 * update html for production files
 */
gulp.task('html-prod', function() {
    return gulp.src([paths.html], {base: './'})
        .pipe(htmlreplace({
            css: {
                src: 'index.min.css',
                tpl: '<link rel="stylesheet" href="{{url_for("static", filename="css/%s")}}" type="text/css">'
            },
            js: {
                src: 'index.min.js',
                tpl: '<script src="{{ url_for("static", filename="js/%s") }}"></script>'
            }
        }))
        .pipe(gulp.dest('./'));
});

/**
 * git tasks
 */
gulp.task("git-merge", function() {
    // switch to production branch
    git.checkout('production', function (err) {
        if (err) throw err;
    });

    git.merge('master', function (err) {
        if (err) throw err;
    });
    return;
})

gulp.task('git-assets', function() {
    return gulp.src([paths.prod_css, paths.prod_js, paths.html])
        .pipe(git.add())
        .pipe(git.commit("Production assets"));
})


gulp.task("default", ["build-watch-js"]);
gulp.task("prod", sequence(
        ['css', "scripts-production"],
        ['git-merge'],
        ['css-minify', 'js-minify', 'html-prod'],
        ['git-assets']
    )
);
