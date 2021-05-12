if (typeof global.window == 'undefined') {
    global.window = {
        config: {
            isServerRendered : false,
            siteDomain : 'https://learning.shine.com',
            imageUrl : 'https://static1.shine.com/l/s/react/media/images/',
            resumeShineSiteDomain : 'https://resume.shine.com',
            shineSiteDomain : 'https://mapi.shine.com',
        }
    };
}



module.exports = require('../ssrBuild/server.js')