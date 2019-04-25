const rewire = require('rewire');
const defaults = rewire('react-scripts/scripts/build.js');
let config = defaults.__get__('config');
var sass = require("node-sass");
var sassUtils = require("node-sass-utils")(sass);


config.optimization.splitChunks = {
    cacheGroups: {
        default: false,
    },
};
// Move runtime into bundle instead of separate file
config.optimization.runtimeChunk = false;

// JS
config.output.filename = '../../../careerplus/static_core/react/dist/desktop/main.js';
// CSS. "5" is MiniCssPlugin
config.plugins[5].options.filename = '../../../careerplus/static_core/react/dist/desktop/main.css';


console.log('-----config======', config.module.rules[2]['oneOf'][5]['use'][3]['options']);


config.module.rules[2]['oneOf'][5]['use'][3]['options'] = {
    ...config.module.rules[2]['oneOf'][5]['use'][3]['options'],
    ...{
        functions: {
            "get($keys)": function (keys) {
                console.log('---keys----', keys.getValue());
                keys = keys.getValue().split(".");
                console.log('--dot keys---', keys);
                // let i;
                // for (i = 0; i < keys.length; i++) {
                //     result = result[keys[i]];
                // }
                // result = sassUtils.castToSass(result);
                // return result;
                let result = 'url(/media/static/react/assets/images/sprite1.svg)'
                result = sassUtils.castToSass(result);

                return result;

            }
        }
    }
}