import React from 'react';
import {renderToString} from 'react-dom/server';
import {Provider} from 'react-redux';
import {StaticRouter} from 'react-router-dom';
import {renderRoutes} from 'react-router-config';

var path = require('path');
const fs = require('fs');

export default (pathname, store, routes, context, timeStamp, staticUrl, isMobile) => {

    const content = renderToString( < Provider
    store = {store} >
        < StaticRouter
    location = {pathname}
    context = {context} >
        < div > {renderRoutes(routes)} < /div>
        < /StaticRouter>
        < /Provider>);
    const cssUrl = isMobile ? `${staticUrl}react/dist/mobile/main-${timeStamp}.css` : `${staticUrl}react/dist/desktop/main-${timeStamp}.css`
    const jsBuildUrl = isMobile ? `${staticUrl}react/dist/mobile/main-${timeStamp}.js` : `${staticUrl}react/dist/desktop/main-${timeStamp}.js`
    return `
  <!DOCTYPE html>
      <html lang="en">
      <head>
        <base href="${"/resume-builder/"}" />
         <link type="text/css" href="${cssUrl}" rel="stylesheet" />
         <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css"
              integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf"
              crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" charset="UTF-8"
              href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick.min.css"/>
        <link rel="stylesheet" type="text/css"
          href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick-theme.min.css"/>
        <link type="text/css" href="${staticUrl}shinelearn/css/resume-builder/resume6.css" rel="stylesheet">
        <meta charset="UTF-8">
        <title>${context.title}</title>
      </head>
      <body>
      <div id="react-app">${content}</div>
      <script>
        window.INITIAL_STATE = ${JSON.stringify(store.getState())}
      </script>
      <script type="text/javascript" src="${jsBuildUrl}"></script>
      </body>
      </html>
  `;

};