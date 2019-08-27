import React from 'react';
import {renderToString} from 'react-dom/server';
import {Provider} from 'react-redux';
import {StaticRouter} from 'react-router-dom';
import {renderRoutes} from 'react-router-config';

var path = require('path');
import {routes} from '../src/routes/index';
import {matchRoutes} from 'react-router-config';


const fs = require('fs');

export default (pathname, store, context, timeStamp) => {

    const content = renderToString( < Provider
    store = {store} >
        < StaticRouter
    location = {pathname}
    context = {context} >
        < div > {renderRoutes(routes)} < /div>
        < /StaticRouter>
        < /Provider>);
    return `
  <!DOCTYPE html>
      <html lang="en">
      <head>
        <base href="${"/"}" />
         <link type="text/css" href="https://learning1.shine.com/careerplus/static_core/react/dist/desktop/client/main-1566912650874.css" rel="stylesheet" />
         <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css"
              integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf"
              crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" charset="UTF-8"
              href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick.min.css"/>
        <link rel="stylesheet" type="text/css"
          href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick-theme.min.css"/>
        <link type="text/css" href="{% static 'shinelearn/css/resume-builder/resume6.css' %}" rel="stylesheet">
        <meta charset="UTF-8">
        <title>Title</title>
      </head>
      <body>
      <div>Time Stamp is ${timeStamp}</div>
      <div id="react-app">${content}</div>
      <script>
        window.INITIAL_STATE = ${JSON.stringify(store.getState())}
      </script>
      <script type="text/javascript"   src="https://learning-static-staging-189607.storage.googleapis.com/l1/s/react/dist/desktop/main-1566912650874.js" defer></script>
      </body>
      </html>
  `;

};