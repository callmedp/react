if (typeof global.window == 'undefined') {
    global.window = {
        config: {
            isServerRendered : true,
            siteDomain : 'http://127.0.0.1:8000',
            imageUrl : '/media/images/',
            resumeShineSiteDomain : 'https://resume.shine.com',
            shineSiteDomain : 'https://mapi.shine.com',
        }
    };
}



module.exports = require('../ssrBuild/server.js')


