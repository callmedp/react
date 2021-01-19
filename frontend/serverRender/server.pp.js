if (typeof global.window == 'undefined') {
    global.window = {
        config: {
            isServerRendered : false,
            siteDomain : 'https://pp-learning.shine.com',
            imageUrl : 'https://static1.shine.com/l/s/media/images/',
            resumeShineSiteDomain : 'https://pp-resume.shine.com',
        }
    };
}



module.exports = require('../ssrBuild/server.js')