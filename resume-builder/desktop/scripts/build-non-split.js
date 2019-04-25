const rewire = require('rewire');
const defaults = rewire('react-scripts/scripts/build.js');
let config = defaults.__get__('config');

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