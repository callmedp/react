import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux'
import store from './store/index';
import App from './App';
import './styles/main.scss';



const rootElement = document.getElementById('root');


ReactDOM.render( <Provider store={store}>
    <App/>
    </Provider>, rootElement)
;
