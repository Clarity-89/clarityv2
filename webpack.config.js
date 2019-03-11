var webpack = require('webpack');
var paths = require('./build/paths');
var MiniCssExtractPlugin = require("mini-css-extract-plugin");

var extractMainCss = new MiniCssExtractPlugin({
    filename: '../css/screen.css'
});


var extractPrintCss = new MiniCssExtractPlugin({
    filename: '../css/print.css'
});

// Separate loader for styles with Bootstrap
var extractBSCss = new MiniCssExtractPlugin({
    filename: '../css/style.css'
});

var extractConfig = {
    fallback: 'style-loader',
    use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
};
/**
 * Webpack configuration
 * Run using "webpack"
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
                use: extractConfig.use
            }, {
                test: /screen\.(css|sass|scss)$/,
                use: extractConfig.use
            }, {
                test: /style\.(css|sass|scss)$/,
                use: extractConfig.use
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    'file-loader'
                ]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                        cacheDirectory: true,
                    }
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                loader: 'url-loader'
            }
        ]
    },

    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: '../css/[name].css'
        })
    ],

    devtool: 'inline-source-map',

    // Minify output
    optimization: {
        minimize: false
    },
};
