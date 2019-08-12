import React from 'react';
import { renderToString } from 'react-dom/server';
import { Provider } from 'react-redux';
import { StaticRouter } from 'react-router-dom';
import { renderRoutes } from 'react-router-config';
import App from '../src/App'

export default (pathname, store, context) => {
  const content = renderToString(
    <App/>
  );


  return `
  <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>Title</title>
      </head>
      <body>
      
      <div id="react-app">${content}</div>
      <script>
        window.INITIAL_STATE = ${JSON.stringify(store.getState())}
      </script>
      </body>
      </html>
  `;
};