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

const timestamp = fs.readFileSync('/tmp/react_build_version.txt', "utf8");


if (typeof window == 'undefined') {
    global.window = {}
}

if (typeof fetch == 'undefined') {
    global.fetch = require('node-fetch');
}

if (typeof localStorage == 'undefined') {
    global.localStorage = {
        setItem: (param1, param2) => {
            return null;
        },
        getItem: (param1) => {
            return null;
        },
        clear: () => {
            return null;
        }
    }
}
console.log('000000', process.argv[0]);
const PORT = process.env.PORT || 8079;
const app = express();

app.use(function (req, res, next) {
    console.log('----', req.path);
    next();
});
app.use('/media', express.static('public'));

app.get('*', async (req, res) => {
    const result = []
    for (const [index, {route}] of (matchRoutes(routes, req.path)||[]).entries()) {
        if (route && route.component && route.component.fetching) {
            console.log('---routes----', route.component.fetching);
            if (index == 0) {
                await route.component.fetching(store, {
                    "email": 'kharbpriya5@gmail.com',
                    "password": "qwerty"
                });
            } else {
                await route.component.fetching(store)
            }
        }
    }
    const context = {}

    const content = render(req.path, store, context, timestamp);
    res.send(content);
});

app.listen(PORT, () => console.log(`Frontend service listening on port: ${PORT}`));