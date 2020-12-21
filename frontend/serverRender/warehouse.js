
import ReactDOMServer from 'react-dom/server';
import { StaticRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from 'store/index';
import React from 'react';
import { renderRoutes } from 'react-router-config';

const render = (req, routes) => {
    const context = { serverRender: true }
    const app = ReactDOMServer.renderToString(
        < Provider store={store}>
            <StaticRouter location={req.url} context={context}>
                {renderRoutes(routes)}
            </StaticRouter>
        </ Provider>
    );

    return app;
}

const expressRoutes = [
    '/courses/:func/:skill/:id/',
]








export {
    render,
    expressRoutes,
} 