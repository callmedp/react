import React from 'react';
import MobileAppRouter from 'routes/index.mobile';
import './App.mobile.css';
import './styles-mobile/main.scss';
import { slide as Menu } from 'react-burger-menu';

function MobileApp() {
  return (
    <div id="outer-container">
        <Menu pageWrapId={ "page-wrap" } outerContainerId={ "outer-container" } />
        <main id="page-wrap">
          <MobileAppRouter />
        </main>
    </div>
  );
}

export default MobileApp;
