import React from 'react';
import ReactDOM from 'react-dom';
import './styles/bootstrap.scss';
import App from './App';
import store from './store/index';
import { Provider } from 'react-redux'; 

ReactDOM.render(<Provider store={store} >
    <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/alertifyjs@1.13.1/build/css/alertify.min.css"/>
    <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/alertifyjs@1.13.1/build/css/themes/default.min.css"/>
    <App /></Provider>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
