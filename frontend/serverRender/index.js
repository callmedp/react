'use strict';
require('isomorphic-fetch');
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

let userAgents, indexFile, appContent, routes, result;

app.use(function (req, res, next) {
    userAgents = req.headers['user-agent'];
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
        indexFile = 'index.mobile';
        routes = require('routes/index.mobile').routes;

    }
    else {

        console.log("<><><><><><>Entered Desktop<><><><><><>  ", req.url)
        indexFile = 'index';
        routes = require('routes/index.desktop').routes;

    }

    const branch = matchRoutes(routes, req.path) || []


    branch.forEach(async ({ route, match }) => {
        if (route && route.actionGroup) {
            try {
                result = await new Promise((resolve, reject) => fetchApiData(store, match.params, route.actionGroup, resolve, reject));
            }
            catch (error) {
                if (error?.status === 404) {
                    return res.redirect('/404/');
                }
            }


            appContent = render(req, routes);

            // const helmet = Helmet.renderStatic();
            // let metaTitlesAll = "";

            // try {
            //     metaTitlesAll += '<title>' + helmet.title.toComponent()[0].key + '</title>';
            //     metaTitlesAll += '<link rel="canonical" href= ' + helmet.link.toComponent()[0].props.href + ' />';

            //     for (let m = 0; m < helmet.meta.toComponent().length; m++) {
            //         let metaTitles = helmet.meta.toComponent()[m].props;

            //         if(metaTitles.name && metaTitles.name === 'description') metaTitlesAll += '<meta name="'+ metaTitles.name +'" content="' + metaTitles.content + '" />';

            //         else if(metaTitles.property && (metaTitles.property === 'og:title' || metaTitles.property === 'og:url' || metaTitles.property === 'og:description' || metaTitles.property === 'og:type' || metaTitles.property === 'og:site_name' || metaTitles.property === 'fb:profile_id')) metaTitlesAll += '<meta property="' +metaTitles.property+ '" content="' + metaTitles.content + '" />';

            //         else if(metaTitles.itemprop && (metaTitles.itemprop === '' || metaTitles.itemprop === 'url' || metaTitles.itemprop === 'description')) metaTitlesAll += '<meta itemprop="' +metaTitles.name+ '" content="' + metaTitles.content + '" />';
            //     }
            // }
            // catch (e) {
            //     // pass
            // }

            // Grab the initial state from our Redux store at send it to the browser to hydrate the app.
            const preloadedState = store.getState()

            return res.render(indexFile, {
                appContent,
                preloadedState: JSON.stringify(preloadedState).replace(/</g, '\\u003c'),
                config: JSON.stringify(window.config)
            });



        }

    });


});



app.get('*', (req, res) => {

    window.config.isServerRendered = false

    if (isMobile(userAgents)) {
        console.log("************Entered Mobile***********", req.url)
        indexFile = 'index.mobile.html';
    }
    else {
        console.log("************Entered Desktop***********", req.url)
        indexFile = 'index.html';
    }
   
    return res.render(indexFile, {
        config: JSON.stringify(window.config)
    });

});


app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
