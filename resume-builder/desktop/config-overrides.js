const fs = require('fs');
var sass = require("node-sass");
var sassUtils = require("node-sass-utils")(sass);
module.exports = (config, env) => {

    fs.writeFile('test.txt', JSON.stringify(config.module.rules[2]['oneOf'][5]['use'][3]['options']), function (err) {
        console.log('----', err);
    });


    const result = {
        'sprite': 'url(/media/static/react/assets/images/sprite.svg)',
        'top-banner': 'url(/media/static/react/assets/images/banner-bg.jpg)',
        'banner-bg': 'url(/media/static/react/assets/images/home-bg.jpg)',
        'logo': 'url(/media/static/react/assets/images/logo.png)'
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