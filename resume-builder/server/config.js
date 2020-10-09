require('@babel/register')({
    presets: ['es2015', 'react']
})
const dotenv = require('dotenv');

dotenv.config();
// Import the rest of our application.
module.exports = require('./index.js')