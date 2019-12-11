import React from 'react';
import {hydrate} from 'react-dom';
import {Provider} from 'react-redux'
import store from './store/index';
import App from './App';
import './styles/main.scss';


const rootElement = document.getElementById('react-app');


hydrate( <Provider store={store}>
    <App/>
    </Provider>, rootElement)
;

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
