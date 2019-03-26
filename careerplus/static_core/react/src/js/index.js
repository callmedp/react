import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import store from './store/index';
import App from './App';
import '../styles/index.scss';


const rootElement = document.getElementById('react-app');

ReactDOM.render(
<Provider store={store}>
    <App/>
    </Provider>, rootElement)
;




