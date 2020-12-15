import React from 'react';
import './App.css';
import MobileApp from 'App.mobile';
import DesktopApp from 'App.desktop';

const isMobileDevice = (userAgents) => {
  return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

function App() {
  // const waitForWidgetInitialised = async () =>
  // new Promise(resolve => {
  //       window.$zopim || (function (d, s) {
  //         var z = window.$zopim = function (c) { z._.push(c) }, $ = z.s =
  //             d.createElement(s), e = d.getElementsByTagName(s)[0]; z.set = function (o) {
  //                 z.set.
  //                     _.push(o)
  //             }; z._ = []; z.set._ = []; $.async = !0; $.setAttribute("charset", "utf-8");
  //         $.src = "https://v2.zopim.com/?5xDfzOy1OsJEYM1rLRdXyvsf3GOj6Qmb"; z.t = +new Date; $.
  //             type = "text/javascript"; e.parentNode.insertBefore($, e)
  //       })(document, "script");

  //       window.$zopim(function() {
  //           window.$zopim.livechat.hideAll();
  //           resolve(true);
  //       });
  // });

  if(isMobileDevice(navigator.userAgent))
    return <MobileApp />
  else
    return <DesktopApp />
}

export default App;
