import React from 'react';
import './App.css';
import MobileApp from 'App.mobile';
import DesktopApp from 'App.desktop';

const isMobileDevice = (userAgents) => {
  return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

function App() {

  if(isMobileDevice(navigator.userAgent))
    return <MobileApp />
  else
    return <DesktopApp />
}

export default App;
