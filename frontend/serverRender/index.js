'use strict';
require('isomorphic-fetch');
const path = require('path');
require('dotenv').config({ 
    path: path.resolve(process.cwd(), '.env.ssr')
})

const fs = require('fs');
const express = require('express');
const matchRoutes = require('react-router-config').matchRoutes;
const fetchApiData = require('utils/fetching').default;

const PORT = process.env.PORT || 8079;
const app = express();

if (typeof global.window == 'undefined') {
    global.window = {
        config: {
            isServerRendered : true,
            siteDomain : process.env.SITE_DOMAIN,
            imageUrl : process.env.IMAGE_URL,
            resumeShineSiteDomain : process.env.RESUME_SHINE_SITE_DOMAIN,
        }
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

const render = require('./warehouse').render;
const expressRoutes = require('./warehouse').expressRoutes;
const store = require('store/index').default;

let userAgents, indexFile, appContent, routes, result;

app.use(function (req, res, next) {
    userAgents = req.headers['user-agent'];
    next();
});

app.use('/media/static/',express.static('../careerplus/media/static/'));
app.use(express.static('../careerplus/media/static/react/'));

const isMobile = (userAgents) => {
    return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

app.get(expressRoutes, (req, res) => {

    if (isMobile(userAgents)) {

        console.log("<><><><><><>Entered Mobile<><><><><><>")
        indexFile = path.resolve('ssrBuild/index.mobile.html');
        routes = require('routes/index.mobile').routes;

    }
    else {

        console.log("<><><><><><>Entered Desktop<><><><><><>")
        indexFile = path.resolve('ssrBuild/index.html');
        routes = require('routes/index.desktop').routes;

    }

    const branch = matchRoutes(routes, req.path) || []
    
    
    branch.forEach(async ({ route, match }) => {
        if (route && route.actionGroup) {
            try {
                result = await fetchApiData(store, match.params, route.actionGroup);
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
                
            
                fs.readFile(indexFile, 'utf8', (err, data) => {
                    if (err) {
                        console.error('Something went wrong:', err);
                        return res.status(500).send('Oops, better luck next time!');
                    }
            
                    return res.send(
                        data.replace('<div id="root"></div>', 
                        `<div id="root">${appContent}</div>
                        <script>
                            window.__PRELOADED_STATE__ = ${JSON.stringify(preloadedState).replace(/</g,'\\u003c')}
                            window.config = ${JSON.stringify(window.config)}
                        </script>`
                        )
                         // .replace('</head>', `${metaTitlesAll}</head>`)
                        );
                });
                
            }
            catch(e){
                console.log("failed to fetch server api", e);
            }
        }

    });
   

});



app.get('*', (req, res) => {
    if(isMobile(userAgents)){
        res.sendFile(path.resolve('ssrBuild/index.mobile.html'));
    }
    else{
        res.sendFile(path.resolve('ssrBuild/index.html'));
    }
});


app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
