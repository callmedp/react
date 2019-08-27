require('@babel/register')({
    presets: ['es2015', 'react']
})

// Import the rest of our application.
module.exports = require('./index.js')