var browserify = require("browserify");
var watchify = require("watchify");
var source = require("vinyl-source-stream");
var buffer = require("vinyl-buffer");
var _ = require("underscore");
var gulp = require("gulp");
var gutil = require('gulp-util');
var nib = require('nib');
var stylus = require('gulp-stylus');
var useref = require('gulp-useref');
var plugins = require('gulp-load-plugins')();
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var git = require('gulp-git');
var path = require('path');
var size = require('gulp-size');
var sequence = require('run-sequence');
var minify_css = require('gulp-minify-css');
var rename = require("gulp-rename");

var paths = {
    //"scripts_dst": "public/js"
    "scripts_dst": "app/static/js",
    "css_dst": "app/static/css",
    "css_src": "frontend/static/css/index.styl",
    "html": "app/templates/index.html"
}

var onError = function(error) {
    gutil.log(gutil.colors.red(error));
};

/**
 * Build all css files
 */
gulp.task('css', function () {
    gulp.src(paths.css_src)
        .pipe(stylus({use: [nib()]}))
        .pipe(gulp.dest(paths.css_dst));
});

gulp.task('css-minify', function () {
    gulp.src(path.join(paths.css_dst, 'index.css'))
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
gulp.task('js-minify', function() {
    var src = [
        path.join(paths.scripts_dst, 'vendors.js'),
        path.join(paths.scripts_dst, 'app.js')
    ];
    return gulp.src(src)
        .pipe(concat('index.min.js'))
        .pipe(size({ showFiles: true }))
        .pipe(uglify())
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
    var assets = useref.assets();

    return gulp.src([paths.html], {base: './'})
        .pipe(assets)
        .pipe(assets.restore())
        .pipe(useref())
        .pipe(gulp.dest('./'));
});

/**
 * git tasks
 */
gulp.task("git-merge", function() {
    // switch to production branch
    gulp.task('checkout', function(){
        git.checkout('branchName', function (err) {
            if (err) throw err;
        });
    });

    gulp.task('merge', function(){
        git.merge('master', function (err) {
        if (err) throw err;
      });
    });
})


gulp.task("default", ["build-watch-js"]);
gulp.task("prod", function(callback) {
    sequence(['css', 'build-js']
        ['git-merge'],
        callback
    );
})
