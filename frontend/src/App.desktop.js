import React, { useEffect }from 'react';
import DesktopAppRouter from './routes/index.desktop';
import { initZendesk } from './utils/zendeskIniti';


function DesktopApp(props) {

  useEffect(()=>{
      initZendesk()
  },[])

  return (
    <DesktopAppRouter/>
  );
}

export default DesktopApp;
