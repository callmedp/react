'use strict';

const path = require('path');
const fs = require('fs');
const express = require('express');
const matchRoutes = require('react-router-config').matchRoutes;

import SkillPage from 'components/DesktopComponent/Core/SkillPage/skillPage';

const PORT = process.env.PORT || 3216;
const app = express();

if (typeof global.window == 'undefined') {
    global.window = {
        config: {}
    };
}

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

const renderDesktop = require('./render').RenderDesktop;
const renderMobile = require('./render').RenderMobile;
const store = require('store/index').default;

let userAgents, indexFile, appContent, routes;

app.use(function (req, res, next) {
    userAgents = req.headers['user-agent'];
    next();
});

app.use('/media/static/', express.static('../careerplus/media/static/'));

const isMobile = (userAgents) => {
    return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

app.get('*', async (req, res) => {

    if (isMobile(userAgents)) {

        indexFile = path.resolve('serverRender/index.mobile.html');
        appContent = renderMobile(req);
        routes = require('routes/index.mobile').routes;
    }

    else {

        indexFile = path.resolve('serverRender/index.html');
        routes = require('routes/index.mobile').routes;
        appContent = renderDesktop(req, routes);
    }
    
    // const branch = matchRoutes(routes, req.path)
    
    // console.log("request header ", req)
    for (const [index, { route, match }] of (matchRoutes(routes, req.path) || []).entries()) {
        if (route && route.staticComponent && route.staticComponent.fetching) {
            try {
                const result = await route.staticComponent.fetching(store, match.params);
                console.log("result is ", result)
            } catch (e) {
                console.log("Error in Api", e);
            }
        }
    }

    console.table(SkillPage)
    
 
    
    fs.readFile(indexFile, 'utf8', (err, data) => {
        if (err) {
            console.error('Something went wrong:', err);
            return res.status(500).send('Oops, better luck next time!');
        }

        return res.send(
            data.replace('<div id="root"></div>', `<div id="root">${appContent}</div>`)
        );
    });

});




app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});