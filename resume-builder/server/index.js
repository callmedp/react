import "regenerator-runtime/runtime";
import express from 'express';
import {matchRoutes} from 'react-router-config';

var path = require('path');


import render from './render';

const fs = require('fs');

const timestamp = process.argv && process.argv.length && process.argv[2] || null;

let userAgents = '', store, routes, isMobile = false;

if (typeof window == 'undefined') {
    global.window = {
        config: {
            staticUrl: process.env.STATIC_URL || '',
            siteDomain: process.env.SITE_DOMAIN || '',
            msiteDomain: process.env.MSITE_DOMAIN || ''
        },
    }
}

if (typeof fetch == 'undefined') {
    global.fetch = require('node-fetch');
}

if (typeof localStorage == 'undefined') {
    global.localStorage = {
        setItem: (param1, param2) => {
            return global.localStorage[param1] = param2;
        },
        getItem: (param1) => {
            return global.localStorage[param1];
        },
        clear: () => {
            return null;
        },
        candidateId: "53461c6e6cca0763532d4b09",
        token: "da3b4f42ce9c2c5cd1d2d81750ca7db51c71e645"
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

    } else {
        console.log('<><><>in desktop');
        store = require('../desktop/src/store/index').default;
        routes = require('../desktop/src/routes/index').routes;
        isMobile = false;
    }

    for (const [index, {route}] of (matchRoutes(routes, req.path) || []).entries()) {
        console.log('-----index, route', index, route);
        if (route && route.component && route.component.fetching) {
            try {
                result = await route.component.fetching(store, {
                    "alt": "Ew4ZExoWCggBB00hHwsZCBRIGw4VGk1STFBJAk4DTgIbB0hWTlVNUkoCTANIXwRTSFdBUUFXSVNIU0tVSBoABwAH"
                });
                context['title'] = result[1];
            } catch (e) {
                console.log("Error in Api", e);
            }
        }
    }
    // console.log('result ====', result, context);

    const content = render(req.path, store,routes, context, timestamp, window.config.staticUrl, isMobile);
    res.send(content);
});

app.listen(PORT, () => console.log(`Frontend service listening on port: ${PORT}`));