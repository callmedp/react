
import ReactDOMServer from 'react-dom/server';
import AppDesktop from 'App.desktop';
import AppMobile from 'App.mobile';
import { StaticRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from 'store/index';
import React from 'react';
import { renderRoutes } from 'react-router-config';

export const RenderDesktop = (req, routes) => {
    const context = {}
    const app = ReactDOMServer.renderToString(
        < Provider store={store}>
            <StaticRouter location={req.url} context={context}>
                { renderRoutes(routes) }
            </StaticRouter>
        </ Provider>
    );
    return app;
}


export const RenderMobile = (req) => {
    const context = {}
    const app = ReactDOMServer.renderToString(
        < Provider store={store}>
            <StaticRouter location={req.path} context={context}>
                <AppMobile />
            </StaticRouter>
        </ Provider>
    );
    return app;
}
