import React, { useEffect } from 'react';
import MobileAppRouter from 'routes/index.mobile';
import './styles-mobile/main.scss';
import { slide as Menu } from 'react-burger-menu';

function MobileApp(props) {
  // const { waitForWidgetInitialised } = props
  
  // Zendesk Chat Script Start//
  // useEffect(()=>{
  //   const timer = setTimeout(() => {
  //       waitForWidgetInitialised()
  //     }, 5000);
  //     return () => clearTimeout(timer);
  // },[])
  //Zendesk Chat Script End//

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
