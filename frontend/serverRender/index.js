'use strict';
global.fetch = require('node-fetch');

// const fetch = require('isomorphic-fetch');
let Promise = require("bluebird");

const path = require('path');

const fs = require('fs');
const express = require('express');
const matchRoutes = require('react-router-config').matchRoutes;
const fetchApiData = require('./fetching').default;

const PORT = process.env.PORT || 8079;
const app = express();

if (typeof global.localStorage == "undefined") {

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




if (typeof global.sessionStorage == 'undefined') {
    global.sessionStorage = {
        setItem: (param1, param2) => {
            return global.sessionStorage[param1] = param2;
        },
        getItem: (param1) => {
            return global.sessionStorage[param1];
        },
        clear: () => {
            let dummyObj = {
                ...{},
                ...global.sessionStorage
            };
            Object.keys(dummyObj).forEach(el => {
                if (['setItem', 'getItem', 'removeItem', 'clear'].findIndex(el) === -1) {
                    delete global.sessionStorage[el];
                }
            })

        },
        removeItem: (param1) => {
            delete global.sessionStorage[param1]
        }

    }
}

const render = require('./warehouse').render;
const expressRoutes = require('./warehouse').expressRoutes;
const store = require('store/index').default;

let userAgents, indexFile, appContent, routes, result, cookies;

app.use(function (req, res, next) {
    userAgents = req.headers['user-agent'];
    next();
});

app.use(function (req, res, next) {
    try {
        cookies = req.headers.cookie;
        cookies = cookies.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, '_em_'.length + 1) === ('_em_=')) {
                cookies = cookie.substring('_em_'.length + 1);
                break;
            }
        }
    } catch (err) {
        cookies = '';
        console.log('error in cookie reading', err);
    }

    next();
});

// app.use('/media/static/',express.static('../careerplus/media/static/'));
app.use(express.static('../careerplus/static_core/react/'));

const isMobile = (userAgents) => {
    return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

app.set('view engine', 'ejs');

app.get(expressRoutes, (req, res) => {

    if (isMobile(userAgents)) {
        console.log("<><><><><><>Entered Mobile<><><><><><>   ", req.url)
        indexFile = 'indexMobile';
        routes = require('routes/index.mobile').routes;
    }
    else {
        console.log("<><><><><><>Entered Desktop<><><><><><>  ", req.url)
        indexFile = 'index';
        routes = require('routes/index.desktop').routes;

    }
    const branch = matchRoutes(routes, req.path) || [];

       const data = async () => await new Promise((resolve, reject) => {
        fetch(`${window.config?.siteDomain || 'https://learning.shine.com'}/api/v1/fetch-info/`,
            {
                method: 'POST',
                body: JSON.stringify({ "em": cookies }),
                headers: { 'Content-Type': 'application/json' }
            })
            .then(res => res.json())
            .then(json => {
                console.log('promise resolved');
            })
            .catch(err => console.log(err))
            .finally(() => {
                console.log('here in finally');
                branch.forEach(async ({ route, match }) => {
                    if (route && route.actionGroup) {
                        try {
                            result = await new Promise((resolve, reject) => fetchApiData(store, match.params,cookies, route.actionGroup, resolve, reject));
                        }
                        catch (error) {
                            if (error?.status === 404) {
                                return res.redirect('/404/');
                            }
                            if(error?.redirect_url) {
                                return res.redirect(error.redirect_url);
                            }
                        }

                        appContent = render(req, routes);
                        const preloadedState = store.getState()

                        return res.render(indexFile, {
                            appContent,
                            preloadedState: JSON.stringify(preloadedState).replace(/</g, '\\u003c'),
                            config: JSON.stringify(window.config)
                        });
                    }

                });
            });
        });
    data();
});


app.get('*', (req, res) => {

    window.config.isServerRendered = false

    if (isMobile(userAgents)) {
        console.log("************Entered Mobile***********", req.url)
        indexFile = 'indexMobile';
    }
    else {
        console.log("************Entered Desktop***********", req.url)
        indexFile = 'index';
    }
   
    return res.render(indexFile, {
        appContent: '',
        preloadedState: JSON.stringify(''),
        config: JSON.stringify(window.config)
    });

});


app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
