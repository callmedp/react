const rewire = require('rewire');
const defaults = rewire('react-scripts/scripts/build.js');

let config = defaults.__get__('config');
var sass = require("node-sass");
var sassUtils = require("node-sass-utils")(sass);
var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

config.optimization.splitChunks = {
    cacheGroups: {
        default: false,
    },
};
// Move runtime into bundle instead of separate file
config.optimization.runtimeChunk = false;

const currentTimeStamp = process.argv && process.argv[2] || +new Date();

// JS
config.output.filename = `../../../careerplus/static_core/score-checker/dist/mobile/main-${currentTimeStamp}.js`;
// CSS. "5" is MiniCssPlugin
config.plugins[5].options.filename = `../../../careerplus/static_core/score-checker/dist/mobile/main-${currentTimeStamp}.css`;
config.plugins.push(new BundleTracker({
    path: __dirname,
    filename: '../../../webpack-score-checker-mobile-stats.json'
}))

const result = {
    'staticUrl': process.env.REACT_APP_ENV === 'staging' ?
        'https://learning-static-staging-189607.storage.googleapis.com/l1/s/' : 'https://static1.shine.com/l/s/',
}


config.module.rules[2]['oneOf'][5]['use'][3]['options'] = {
    ...config.module.rules[2]['oneOf'][5]['use'][3]['options'],
    ...{
        functions: {
            "get($keys)": function (keys) {
                keys = keys.getValue();
                let output = result[keys];
                output = sassUtils.castToSass(output);
                return output;

            }
        }
    }
}

