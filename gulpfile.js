const gulp = require("gulp");
const sass = require("gulp-sass")(require('node-sass'));
const paths = require("./build/paths");
const sourcemaps = require("gulp-sourcemaps");
const del = require("del");

const sassFiles = ["style", "print", "screen"].map(
    name => `${paths.sassSrcDir}${name}.scss`
);

function scss(cb) {
    gulp.src(sassFiles)
        .pipe(sourcemaps.init())
        .pipe(
            sass({
                outputStyle: "compressed",
                includePaths: ["./node_modules"]
            }).on("error", sass.logError)
        )
        // write the sourcemaps
        .pipe(sourcemaps.write("./maps"))
        .pipe(gulp.dest(`${paths.cssDir}`));
    cb();
}

function clean(cb) {
    del([paths.cssDir + "*.css"]);
    cb();
}

function watch(cb) {
    gulp.watch(paths.sassSrc, scss);
    cb();
}

exports.watch = watch;
exports.build = gulp.series(clean, scss);
