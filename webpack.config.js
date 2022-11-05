var webpack = require("webpack");
var paths = require("./build/paths");

/**
 * Webpack configuration
 * Run using "webpack"
 */
module.exports = (env, argv) => ({
    // Path to the js entry point (source)
    entry: __dirname + "/" + paths.jsEntry,

    // Path to the (transpiled) js
    output: {
        path: __dirname + "/" + paths.jsDir, // directory
        filename: "app.js" // file
    },

    module: {
        rules: [
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: ["file-loader"]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"],
                        cacheDirectory: true
                    }
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                use: ["url-loader"]
            },
            {
                test: /\.css/,
                use: ["style-loader", {loader: 'css-loader'}],
            }
        ]
    },

    devtool: "inline-source-map",

    // Minify output
    optimization: {
        minimize: argv.mode === 'production'
    },
});
