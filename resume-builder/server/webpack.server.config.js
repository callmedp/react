require('dotenv').config()
const path = require('path');
const webpackNodeExternals = require('webpack-node-externals');
const webpack = require('webpack');
const isDevelopment = true;
const fs = require('fs');

module.exports = env => {


    return {
        mode: 'development',
        target:
            'node',
        entry:
            path.join(__dirname, 'config.js'),
        output:
            {
                path: path.resolve(__dirname),
                filename:
                    'server.js'
            }
        ,
        module: {
            rules: [
                {
                    test: /\.(js|jsx)$/,
                    use: {
                        loader: "babel-loader",
                        options: {
                            presets: ["@babel/preset-env", "@babel/preset-react"]
                        }
                    },
                    exclude: /node_modules/
                },
                {
                    test: /\.(scss|css)$/,
                    loader: "ignore-loader"
                },
                {
                    test: /\.css$/,
                    use: ['style-loader', 'css-loader']
                }

            ]
        }
        ,

        resolve: {
            extensions: [".js", ".jsx", ".json", ".wasm", ".mjs", "*"]
        },
        externals:
            [webpackNodeExternals()]
    };
}

