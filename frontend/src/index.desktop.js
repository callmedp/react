import React from 'react';
import ReactDOM from 'react-dom';
import './styles/bootstrap.scss';
import AppDesktop from './App.desktop';
import { Provider } from 'react-redux';
import store from 'store/index';
import { BrowserRouter } from 'react-router-dom';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';

ReactDOM.hydrate(
  <React.StrictMode>
    <Provider store={store} >
      <BrowserRouter>
        <AppDesktop />
      </BrowserRouter>
    </Provider>

  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorkerRegistration.register();
