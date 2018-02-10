var webpack = require('webpack');
var paths = require('./build/paths');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var extractMainCss = new ExtractTextPlugin({
    filename: '../css/screen.css'
});


var extractPrintCss = new ExtractTextPlugin({
    filename: '../css/print.css'
});

/**
 * Webpack configuration
 * Run using "webpack" or "gulp js"
 */
module.exports = {
    // Path to the js entry point (source)
    entry: __dirname + '/' + paths.jsEntry,

    // Path to the (transpiled) js
    output: {
        path: __dirname + '/' + paths.jsDir, // directory
        filename: 'app.js', // file
    },

    module: {
        rules: [
            {
                test: /print\.(css|sass|scss)$/,
                use: extractPrintCss.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'sass-loader']
                })
            },
            {
                test: /screen\.(css|sass|scss)$/,
                use: extractMainCss.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'sass-loader']
                })
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    'file-loader'
                ]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                        cacheDirectory: true,
                    }
                }
            },
        ]
    },

    devtool: 'eval-source-map',

    // Minify output
    plugins: [
        new webpack.optimize.UglifyJsPlugin({minimize: true}),
        extractMainCss, extractPrintCss
    ],

    watch: true
};
