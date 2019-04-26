const fs = require('fs');
var sass = require("node-sass");
var sassUtils = require("node-sass-utils")(sass);
module.exports = (config, env) => {

    const result = {
        'staticUrl': '/media/static/',
    };

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
    };

    return config
}