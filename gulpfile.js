'use strict';
/*! dockdj tasks
 * @author Ron. A @0xADADA
 * MIT License
 */

var autoprefixer = require('gulp-autoprefixer'),
    csslint = require('gulp-csslint'),
    gulp = require('gulp'),
    minifyCss = require('gulp-minify-css'),
    rev = require('gulp-rev'),
    revReplace = require('gulp-rev-replace'),
    sass = require('gulp-sass'),
    sourceMaps = require('gulp-sourcemaps'),
    browserSync = require('browser-sync').create(),
    reload = browserSync.reload;

var config = {
    autoprefixer: {
        browsers: [
            'last 2 versions',
            '> 5%'
        ]
    },
    csslint: {
        csslintrc: '.csslintrc.json',
        src: [
            'app/apps/*/static/**/*.css',
            '!app/apps/*/static/vendor/**/*'
          ]
    },
    minifyCss: {
        options: {
            keepBreaks  : false,
            advanced    : false,
            rebase      : false,
            debug       : true
        }
    },
    revReplace : {
        manifest: 'app/dist/stylesheets/rev-manifest.json',
        template: 'app/apps/base/templates/base/base.html',
        templateDir: 'app/apps/base/templates/base/'
    },
    sass: {
        src: 'app/apps/webroot/static/stylesheets/all.scss',
        dest: 'app/dist/stylesheets',
        options: {
            style: 'compressed',
            precision: 8
        }
    },
    browserSync: {
        proxy: '<192.168.59.nn>' /* Set by 'run:browser-sync' */
    },
    watch: {
        sassSrc: ['app/apps/*/static/**/*.scss']
    }
};


// check:css CSS syntax checking with CSSLint.
gulp.task('check:css', function() {
    return gulp.src(config.csslint.src)
        .pipe(csslint(config.csslint.csslintrc))
        .pipe(csslint.reporter('compact'))
        .pipe(csslint.reporter('fail'));
});

// check:python runs PEP257 linting on all app python code
gulp.task('check:python', function() {
    require('child_process')
    .spawn('pep257', [
            "--match-dir='(?!migrations).*'",
            'app/apps'
        ],
        { stdio: 'inherit' }
    );
});

// test:unit runs Python unit tests
gulp.task('test:unit', function() {
    var child_process = require('child_process'),
        proc = child_process.spawnSync('./bin/test', [
            ],
            { stdio: 'inherit' }
        );
    if( proc.status !== 0 ) {
        console.log('test:unit exited with code', proc.status);
        process.exit(proc.status);
    }
});

// Sass post-processing
gulp.task('sass', function () {
    return gulp.src(config.sass.src)
        .pipe(sourceMaps.init())
        .pipe(
            sass(config.sass.options)
            .on('error', sass.logError)
        )
        .pipe(autoprefixer({
            browsers: config.autoprefixer.browsers
        }))
        .pipe(minifyCss(config.minifyCss.options))
        .pipe(browserSync.stream()) // send assets to browser-sync
        .pipe(sourceMaps.write('sourcemaps')) // write sourcemaps
        .pipe(gulp.dest(config.sass.dest)); // write output files
});

// Sass post-processing with cache busted file-names and updated refs
gulp.task('sass:build', function () {
    return gulp.src(config.sass.src)
        .pipe(sourceMaps.init())
        .pipe(
            sass(config.sass.options)
            .on('error', sass.logError)
        )
        .pipe(autoprefixer({
            browsers: config.autoprefixer.browsers
        }))
        .pipe(minifyCss(config.minifyCss.options))
        .pipe(browserSync.stream()) // send assets to browser-sync
        .pipe(rev())
        .pipe(sourceMaps.write('sourcemaps')) // write sourcemaps
        .pipe(gulp.dest(config.sass.dest)) // write output files
        .pipe(rev.manifest())
        .pipe(gulp.dest(config.sass.dest)); // write manifest
});


// BrowserSync / Livereload
gulp.task('browser-sync', function() {
    browserSync.init({
        proxy: config.browserSync.proxy
    });
    gulp.watch(config.watch.sassSrc, ['sass']);
});


/* run:browser-sync:
 * Fetch boot2docker IP from the command line to run browser-sync.
 */
gulp.task('run:browser-sync', function() {
    var exec = require('child_process').exec,
        child;
    child = exec('boot2docker ip',
        function (error, stdout, stderr) {
            // if boot2docker ran without error, run browser-sync
            config.browserSync.proxy = stdout;
            console.log('boot2docker container running at:', stdout)
            // start browser sync
            gulp.start('browser-sync');
        }
    );
});

// Watch task
gulp.task('watch', function() {
    gulp.watch(config.watch.sassSrc, ['sass']);
});


/* collectstatic
 * Django asset pipeline tool that moves app assets to dist/ directory.
 */
gulp.task('collectstatic', function() {
    require('child_process')
    .spawn('./app/manage.py', [
            'collectstatic',
            '--noinput'
        ],
        { stdio: 'inherit' }
    );
});


/* revreplace
 * Updates links to any cache-busted assets.
 */
gulp.task("revreplace", ['collectstatic','sass:build'], function() {
    var revManifest = gulp.src(config.revReplace.manifest);
    return gulp.src(config.revReplace.template)
        .pipe(revReplace({ manifest: revManifest}))
        .pipe(gulp.dest(config.revReplace.templateDir));
});


/* check
 * Code quality testing.
 */
gulp.task('check', ['check:css', 'check:python']);


/* test
 * Javascript unit tests, Python unit tests and selenium browser tests
 */
gulp.task('test', ['test:unit']);


/* default task
 * Prepares assets and moves them into the dist/ directory.
 */
gulp.task('default', ['check', 'sass', 'collectstatic']);


/* connect
 * Calls the default task and opens a browser-sync browser window.
 */
gulp.task('connect', ['default', 'run:browser-sync']);

/* build task
 * Runs csslint, jshint, jasmine tests.
 * Translates SASS to CSS, concatenates & minifies.
 * Writes source maps and rev'es file names.
 * Updates base template to refer to the rev'ed assets.
 */
gulp.task('build', ['check', 'test', 'revreplace']);
