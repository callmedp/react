import React, { useEffect } from 'react';
import MobileAppRouter from 'routes/index.mobile';
import './styles-mobile/main.scss';
import { slide as Menu } from 'react-burger-menu';
import { initZendesk } from './utils/zendeskIniti';

function MobileApp(props) {

  useEffect(()=>{
    const timer = setTimeout(() => {
       initZendesk()
      }, 5000);
      return () => clearTimeout(timer);
  },[])

  return (
    <div id="outer-container">
        <Menu pageWrapId={ "page-wrap" } outerContainerId={ "outer-container" } />
        <main id="page-wrap">
          <MobileAppRouter/>
        </main>
    </div>
  );
}

export default MobileApp;
