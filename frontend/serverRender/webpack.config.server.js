const webpackNodeExternals = require("webpack-node-externals");
const path = require('path');
const fs = require('fs');
const CopyPlugin = require("copy-webpack-plugin");

const moduleFileExtensions = [
    '.web.mjs',
    '.mjs',
    '.web.js',
    '.js',
    '.web.ts',
    '.ts',
    '.web.tsx',
    '.tsx',
    '.json',
    '.web.jsx',
    '.jsx',
];

const appDirectory = fs.realpathSync(process.cwd());
const resolveApp = relativePath => path.resolve(appDirectory, relativePath);

const resolveModule = (resolveFn, filePath) => {
    const extension = moduleFileExtensions.find(extension =>
        fs.existsSync(resolveFn(`${filePath}.${extension}`))
    );

    if (extension) {
        return resolveFn(`${filePath}.${extension}`);
    }

    return resolveFn(`${filePath}.js`);
};

const serverIndexJs = resolveModule(resolveApp, 'serverRender/index');
const serverBuild = resolveApp('./ssrBuild');


const entry = [serverIndexJs];

const output = {
    path: serverBuild,
    filename: 'server.js',
}

const externals = [
    webpackNodeExternals(),
]

const resolve = {
    extensions: moduleFileExtensions,
    modules: [path.resolve(__dirname, '../src')]
}


const Module = {
    rules: [
        { test: /\.(js|jsx)$/, use: 'babel-loader' },
        { test: /\.(scss|css)$/, loader: "ignore-loader"},
    ]
}

const plugins = [
    new CopyPlugin({
        patterns: [
            { from: path.resolve(__dirname, '../ssrBuild/media'), 
                to: path.resolve(__dirname, '../../careerplus/static_core/react/media') 
            },
          ]
        })
]

module.exports = {
    mode : 'production',
    target : 'node',
    devtool : 'source-map',
    entry,
    output,
    module : Module ,
    resolve,
    plugins,
    externals,
};
