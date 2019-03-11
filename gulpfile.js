const gulp = require('gulp');
const sass = require("gulp-sass");
const paths = require('./build/paths');

gulp.task('sass', () => {
    ['style', 'print', 'screen'].forEach(fileName => {
        gulp.src(`${paths.sassSrcDir}/${fileName}`)
    })
})
