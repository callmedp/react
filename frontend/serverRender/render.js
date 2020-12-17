
import ReactDOMServer from 'react-dom/server';
import AppDesktop from '../src/App.desktop';
import AppMobile from '../src/App.mobile';
import { StaticRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../src/store/index';
import React from 'react';

export const RenderDesktop = (req) => {
    const context = {}
    const app = ReactDOMServer.renderToString(
        < Provider store={store}>
            <StaticRouter location={req.url} context={context}>
                <AppDesktop />
            </StaticRouter>
        </ Provider>
    );
    return app;
}


export const RenderMobile = (req) => {
    const context = {}
    const app = ReactDOMServer.renderToString(
        < Provider store={store}>
            <StaticRouter location={req.url} context={context}>
                <AppMobile />
            </StaticRouter>
        </ Provider>
    );
    return app;
}
