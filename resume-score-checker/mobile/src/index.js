import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { Provider } from 'react-redux';
import store from './stores/index';
import './styles/common.scss';



ReactDOM.render(
    <Provider store = {store}>
        <App />
    </Provider>
    , document.getElementById('root')
);

