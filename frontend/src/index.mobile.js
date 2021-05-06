import React from 'react';
import ReactDOM from 'react-dom';
import './styles/bootstrap.scss';
import AppMobile from './App.mobile';
import { Provider } from 'react-redux';
import store from 'store/index';
import { BrowserRouter } from 'react-router-dom';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';

ReactDOM.hydrate(
  <React.StrictMode>
    <Provider store={store} >
      <BrowserRouter>
      <AppMobile />
      </BrowserRouter>
    </Provider>

  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorkerRegistration.register();

