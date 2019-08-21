import express from 'express';
// import {matchRoutes} from 'react-router-config';
// import render from './render';
// import store from '../src/store/index';
// import {routes} from '../src/routes/index';
var path = require('path');
import store from '../src/store.js';
import render from './render';



const PORT = process.env.PORT || 8079;
const app = express();
app.use('/dist',express.static('dist'));

app.get('*', (req, res) => {
  const content = render(req.path, store, {});
  res.send(content);
});
//
// // app.use('/dist', express.static('dist'));
// // app.use('/img', express.static('img'));
// app.get('/resume-builder/', async (req, res) => {
//
//     const actions = matchRoutes(routes, req.path)
//         .map(async actions => await Promise.all(
//             (actions || []).map(p => p && new Promise(resolve => p.then(resolve).catch(resolve)))
//             )
//         );
//
//     await Promise.all(actions);
//     const context = {};
//     const content = render(req.path, store, context);
//
//     res.send(content);
// });

app.listen(PORT, () => console.log(`Frontend service listening on port: ${PORT}`));