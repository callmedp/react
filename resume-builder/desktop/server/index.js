import "regenerator-runtime/runtime";
import express from 'express';
import {matchRoutes} from 'react-router-config';
// import render from './render';
// import store from '../src/store/index';
// import {routes} from '../src/routes/index';
var path = require('path');
import store from '../src/store/index.js';
import {routes} from '../src/routes/index';

import render from './render';

const fs = require('fs');

const timestamp = process.argv && process.argv.length && process.argv[2] || null;


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
    next();
});
app.use('/resume-builder/dist', express.static('dist'));
app.use('/media/static/react/assets/images', express.static('assets/images'));
app.use('/media/static/resumebuilder/images', express.static('assets/resumebuilder/images'));

app.get('*', async (req, res) => {
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

    const content = render(req.path, store, context, timestamp, window.config.staticUrl);
    res.send(content);
});

app.listen(PORT, () => console.log(`Frontend service listening on port: ${PORT}`));