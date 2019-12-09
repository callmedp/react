import "regenerator-runtime/runtime";
import express from 'express';
import { matchRoutes } from 'react-router-config';

var path = require('path');

import render from './render';

const fs = require('fs');

const timestamp = 3434343434343 //fs.readFileSync(`${process.env.STATIC_FILE_PATH}`, "utf8");

let userAgents = '', store, routes, isMobile = false, paramObj = {
    alt: ''
};


if (typeof window == 'undefined') {
    global.window = {
        config: {
            staticUrl: process.env.STATIC_URL || '',
            siteDomain: process.env.SITE_DOMAIN || '',
            siteProtocol: process.env.SITE_PROTOCOL || '',
        },
        location: {
            href: ''
        }
    };

    global.window.config.siteDomain = `${global.window.config.siteProtocol}://${global.window.config.siteDomain}`;

}


if (typeof fetch == 'undefined') {
    global.fetch = require('node-fetch');
}


if (typeof localStorage == 'undefined') {
    console.log(' in here', global.localStorage);
    global.localStorage = {
        setItem: (param1, param2) => {
            return global.localStorage[param1] = param2;
        },
        getItem: (param1) => {
            return global.localStorage[param1];
        },
        clear: () => {
            let dummyObj = {
                ...{},
                ...global.localStorage
            };
            Object.keys(dummyObj).forEach(el => {
                if (['setItem', 'getItem', 'removeItem', 'clear'].findIndex(el) === -1) {
                    delete global.localStorage[el];
                }
            })
        },
        removeItem: (param1) => {
            delete global.localStorage[param1]
        }
    }
}

const PORT = process.env.PORT || 8079;
const app = express();
let context = {
    'title': ''
}, result;

app.use(function (req, res, next) {
    userAgents = req.headers['user-agent'];
    // import store
    next();
});

app.use('/resume-builder/dist', express.static('dist'));

app.use('/media/static/react/assets/images', express.static('assets/images'));

app.use('/media/static/resumebuilder/images', express.static('assets/resumebuilder/images'));

app.get('*', async (req, res) => {
    const checkIsMobile = (userAgents) => {
        return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
    }
    if (checkIsMobile(userAgents)) {
        console.log('<><><><>in mobile');
        store = require('../mobile/src/store/index').default;
        routes = require('../mobile/src/routes/index').routes;
        isMobile = true;
    }
    else {
        console.log('<><><>in desktop');
        store = require('../desktop/src/store/index').default;
        routes = require('../desktop/src/routes/index').routes;
        isMobile = false;
    }

    for (const [index, { route }] of (matchRoutes(routes, req.path) || []).entries()) {
        if (route && route.component && route.component.fetching) {
            try {
                if (req.query && req.query.token) {
                    paramObj['alt'] = req.query.token
                }
                result = await route.component.fetching(store, paramObj);

                context['title'] = result[result.length - 1];
            } catch (e) {
                console.log("Error in Api", e);
            }
        }
    }

    const content = render(req.path, store, routes, context, timestamp, window.config.staticUrl, isMobile, window.config.siteDomain);
    res.send(content);
});

app.listen(PORT, () => console.log(`Frontend service listening on port: ${PORT}`));

