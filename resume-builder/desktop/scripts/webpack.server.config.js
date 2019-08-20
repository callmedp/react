const path = require('path');
const webpackNodeExternals = require('webpack-node-externals');

console.log('--webpack called--', path.join(__dirname,'..', 'server/index.js'));
module.exports = {
  mode: 'development',
  target: 'node',
  entry: path.join(__dirname, '..', 'server/index.js'),
  output: {
    path: path.resolve(__dirname),
    filename: 'server.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: 'babel-loader',
        exclude: /node_modules/
      },
    ]
  },
  externals: [webpackNodeExternals()]
};