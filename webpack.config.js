var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractText = require('extract-text-webpack-plugin');


module.exports = [{
    entry: path.join(__dirname, 'resume-builder/desktop/src/index'),
    output: {
        path: path.join(__dirname, 'careerplus/static_core/react/dist/desktop'),
        filename: '[name].js'
    },
    plugins: [
        new BundleTracker({
            path: __dirname,
            filename: 'webpack-desktop-stats.json'
        }),
        new ExtractText({
            filename: '[name].css'
        }),
    ],
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                loader: ['style-loader', 'css-loader'],
            },
            {
                test: /\.scss$/,
                use: ExtractText.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'sass-loader']
                })
            },
        ],
    },

}]
