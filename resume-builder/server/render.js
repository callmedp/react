import React from 'react';
import { renderToString } from 'react-dom/server';
import { Provider } from 'react-redux';
import { StaticRouter } from 'react-router-dom';
import { renderRoutes } from 'react-router-config';

var path = require('path');
const fs = require('fs');

export default (pathname, store, routes, context, timeStamp, staticUrl, isMobile, siteDomain) => {

  const content = renderToString(< Provider
    store={store} >
    < StaticRouter
      location={pathname}
      context={context} >
      < div >
        {renderRoutes(routes)}
      </div>
    </StaticRouter>
  </Provider>);
  

  // const cssUrl = isMobile ? `${staticUrl}react/dist/mobile/main-${timeStamp}.css` : `${staticUrl}react/dist/desktop/main-${timeStamp}.css`
  // const jsBuildUrl = isMobile ? `${staticUrl}react/dist/mobile/main-${timeStamp}.js` : `${staticUrl}react/dist/desktop/main-${timeStamp}.js`
  const cssUrl = isMobile ? `dist/main-mobile.css` : `dist/main-desktop.css`,
    jsBuildUrl = isMobile ? `dist/main-mobile.js` : `dist/main-desktop.js`,
    viewPort = isMobile ? `width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no`
      : "width=device-width, initial-scale=1, shrink-to-fit=no";



    //   <script>
    //   var url = "${siteDomain}/api/v1/chatbot/?key=CHATBOT_URL"
    //   fetch(url, {headers : {"Content-Type": "application/json"}, method:'GET'})
    //   .then(response => response.json())
    //   .then(result=> {
    //     console.log("---result--",result);
    //   })
    // </script>
    
  // Meta descriptions 

  // <meta name="description" content="Online Resume Builder, Make your resume with our easy-to-use templates & pro resume tips from experts. Select, Personalize/Customize any built-in resume templates for free download.">
  // <meta name="keywords" content="Resume formats, format of Resume, Download Resume format, CV format">
  // <meta property="og:title" content="${context.title}">
  // <meta property="og:url" content="https://learning.shine.com/cms/resume-format/1/">
  // <meta property="og:description" content="Online Resume Builder, Make your resume with our easy-to-use templates & pro resume tips from experts. Select, Personalize/Customize any built-in resume templates for free download.">
  // <meta property="og:type" content="Website">
  // <meta property="og:site_name" content="ShineLearning">
  // <meta property="article:modified_time" content="2018-07-20 08:52:47.536574+00:00">
  // <meta property="fb:profile_id" content="282244838633660">
  // <meta property="og:image" content="https://static1.shine.com/l/s/shinelearn/images/cms/creative-1.jpg">
  // <meta itemprop="name" content="${context.title}">
  // <meta itemprop="dateModified" content="2018-08-07 08:52:47.536574+00:00">
  // <meta itemprop="url" content="https://learning.shine.com/cms/resume-format/1/">
  // <meta itemprop="description" content="Online Resume Builder, Make your resume with our easy-to-use templates & pro resume tips from experts. Select, Personalize/Customize any built-in resume templates for free download.">
  // <link rel="canonical" href="${siteProtocol}://${siteDomain}/${'resume-builder'}/">


  return `
  <!DOCTYPE html>
      <html lang="en">
      <head>
        <base href="/resume-builder/" />
         <link type="text/css" href="${cssUrl}" rel="stylesheet" />
         <meta name="viewport" content="${viewPort}"/>
         <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css"
              integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf"
              crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" charset="UTF-8"
              href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick.min.css"/>
        <link rel="stylesheet" type="text/css"
          href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick-theme.min.css"/>
        <link type="text/css" href="${staticUrl}shinelearn/css/resume-builder/resume6.css" rel="stylesheet">
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>${context.title}</title>
      </head>
      <body>
      <div id="react-app">${content}</div>
      <script>
        window.__PRELOADED_STATE__ = ${JSON.stringify(store.getState()).replace(/</g, '\\u003c')}
        document.onkeydown = function(e) {
          if(event.keyCode == 123) {
              return false;
          }
          if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)){
              return false;
          }
          if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)){
              return false;
          }
          if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)){
              return false;
          }
      }
      </script>
     
      <script>
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
        ga('create', 'UA-3537905-41', 'auto');
        ga('send', 'pageview');
       </script>
      <script type="text/javascript" src="${jsBuildUrl}"></script>
      </body>
    </html>
  `;

};