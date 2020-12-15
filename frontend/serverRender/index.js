import path from 'path';
import fs from 'fs';

import React from 'react';
import express from 'express';
import ReactDOMServer from 'react-dom/server';

import AppDesktop from '../src/App.desktop';

const PORT = process.env.PORT || 3216;
const app = express();


app.get('*', (req, res) => {
    const app = ReactDOMServer.renderToString(<AppDesktop />);

    const indexFile = path.resolve('../../careerplus/templates/skillPageIndex');

    fs.readFile(indexFile, 'utf8', (err, data) => {
        if (err) {
            console.error('Something went wrong:', err);
            return res.status(500).send('Oops, better luck next time!');
        }

        return res.send(
            data.replace('<div id="root"></div>', `<div id="root">${app}</div>`)
        );
    });
});

app.use(express.static('../../careerplus/'));

app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});