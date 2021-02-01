if (typeof global.window == 'undefined') {
    global.window = {
        config: {
            isServerRendered : false,
            siteDomain : 'https://learning2.shine.com',
            imageUrl : 'https://learning-static-staging-189607.storage.googleapis.com/l2/s/react/media/images/',
            resumeShineSiteDomain : 'https://resume.shine.com',
            shineSiteDomain : 'https://mapi.shine.com',
        }
    };
}



module.exports = require('../ssrBuild/server.js')


