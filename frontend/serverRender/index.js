'use strict';

const path = require('path');
const fs = require('fs');
const express = require('express');



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
let userAgents = '';

app.use(function (req, res, next) {
    userAgents = req.headers['user-agent'];
    next();
});

app.use('/media/static/',express.static('../careerplus/media/static/'));

const isMobile = (userAgents) => {
    return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

app.get('*', (req, res) => {
    console.log("listening request", req.headers['user-agent'] )
    if(isMobile(userAgents)){

        const indexFile = path.resolve('serverRender/index.mobile.html');
        const appContent =renderMobile(req);
        
    
        fs.readFile(indexFile, 'utf8', (err, data) => {
            if (err) {
                console.error('Something went wrong:', err);
                return res.status(500).send('Oops, better luck next time!');
            }
    
            return res.send(
                data.replace('<div id="root"></div>', `<div id="root">${appContent}</div>`)
            );
        });
    }
    else{

    const indexFile = path.resolve('serverRender/index.html');
    const appContent =renderDesktop(req);

    fs.readFile(indexFile, 'utf8', (err, data) => {
        if (err) {
            console.error('Something went wrong:', err);
            return res.status(500).send('Oops, better luck next time!');
        }

        return res.send(
            data.replace('<div id="root"></div>', `<div id="root">${appContent}</div>`)
        );
    });
}
});




app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});