import React, { useEffect }from 'react';
import DesktopAppRouter from './routes/index.desktop';


function DesktopApp(props) {
  const { waitForWidgetInitialised } = props

  // Zendesk Chat Script Start//
  useEffect(()=>{
        waitForWidgetInitialised()
  },[])
  //Zendesk Chat Script End//

  return (
    <DesktopAppRouter/>
  );
}

export default DesktopApp;
