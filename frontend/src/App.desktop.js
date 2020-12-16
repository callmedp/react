import React from 'react';
import DesktopAppRouter from './routes/index.desktop';


function DesktopApp(props) {
  return (
    <DesktopAppRouter isBrowser={props.isBrowser}/>
  );
}

export default DesktopApp;
