import React from 'react';
import { renderToString } from 'react-dom/server';
import { Provider } from 'react-redux';
import { StaticRouter } from 'react-router-dom';
import { renderRoutes } from 'react-router-config';

var path = require('path');
const fs = require('fs');

export default (pathname, store, routes, context, timeStamp, staticUrl, isMobile, siteDomain, siteDomainChat, shineSiteDomain) => {
  
  // const content = renderToString(< Provider
  //   store={store} >
  //   {/* < StaticRouter
  //   location={pathname}
  //   context={context} >
  //   < div >
  //   {renderRoutes(routes)}
  //   </div>
  //   </StaticRouter> */}
  //   </Provider>);
    
    
    const cssUrl = isMobile ? `${staticUrl}react/dist/mobile/main-${timeStamp}.css` : `${staticUrl}react/dist/desktop/main-${timeStamp}.css`;
    const jsBuildUrl = isMobile ? `${staticUrl}react/dist/mobile/main-${timeStamp}.js` : `${staticUrl}react/dist/desktop/main-${timeStamp}.js`;
    const viewPort = isMobile ? `width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no`
    : "width=device-width, initial-scale=1, shrink-to-fit=no";
    
    //  const cssUrl = isMobile ? `dist/main-mobile.css` : `dist/main-desktop.css`,
    //  jsBuildUrl = isMobile ? `dist/main-mobile.js` : `dist/main-desktop.js`;
    
    // Meta descriptions 
    
    const desktopCssUrl = isMobile ? '' : `<link type="text/css" href="${staticUrl}shinelearn/css/resume-builder/resume6.css" rel="stylesheet">`
    
    return `
    <!DOCTYPE html>
    <html lang="en" itemscope itemtype="http://www.schema.org/WebPage">
    <head>
    <base href="/resume-builder/" />
    <title>${context.title}</title>
    <link type="text/css" href="${cssUrl}" rel="stylesheet" />
    <link rel="shortcut icon" href="${staticUrl}shinelearn/images/fav_icon.png"/>
    <meta http-equiv="refresh" content="0;url=https://resumestage.shine.com/resume-builder">
    <meta name="viewport" content="${viewPort}"/>
    <meta name="description" content="Online Resume Builder, Make your resume with our easy-to-use templates & pro resume tips from experts. Select, Personalize/Customize any built-in resume templates for free download.">
    <meta property="og:title" content="${context.title}">
    <meta property="og:url" content="https://resumestage.shine.com/resume-builder">
    <meta property="og:description" content="Online Resume Builder, Make your resume with our easy-to-use templates & pro resume tips from experts. Select, Personalize/Customize any built-in resume templates for free download.">
    <meta property="og:type" content="Website">
    <meta property="og:site_name" content="ShineLearning">
    <meta property="fb:profile_id" content="282244838633660">
    <meta property="og:image" content="https://static1.shine.com/l/s/react/assets/images/home-banner-slider.png">
    <meta itemprop="name" content="${context.title}">
    <meta itemprop="url" content="https://resumestage.shine.com/resume-builder">
    <meta itemprop="description" content="Online Resume Builder, Make your resume with our easy-to-use templates & pro resume tips from experts. Select, Personalize/Customize any built-in resume templates for free download.">
    <link rel="canonical" href="https://resumestage.shine.com/resume-builder">
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css"
    integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf"
    crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" charset="UTF-8"
    href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.6.0/slick.min.css"/>
    ${desktopCssUrl}
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Shine Learning",
      "alternateName": "Resume Builder",
      "url": "https://learning.shine.com/",
      "logo": "https://static1.shine.com/l/s/shinelearn/images/logo.png"
    }
    </script>

    <script>
    console.log('<><><>windows', window.location)
    window.location.href = "https://resumestage.shine.com/resume-builder";
    </script>
    </head>
    <body>
    <script>
    window.__PRELOADED_STATE__ = ${JSON.stringify(store.getState()).replace(/</g, '\\u003c')}
    window.config = {}
    config.staticUrl = "${staticUrl}" 
    config.siteDomain = "${siteDomain}"
    config.siteDomainChat = "${siteDomainChat}"
    config.shineSiteDomain = "${shineSiteDomain}"
    
    </script>
    <script>
    document.oncontextmenu = document.body.oncontextmenu = function() {return false;}
    document.onkeydown = function(e) {
      if(e.keyCode == 123) {
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
      if(e.metaKey && e.altKey && e.keyCode == 'I'.charCodeAt(0) ){
        return false;
      }
      if(e.metaKey && e.altKey && e.keyCode == 'J'.charCodeAt(0) ){
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
  
  
  //<script type="text/javascript" src="https://static1.shine.com/l/cm/chatbot/learning_resume-1588796766.js"></script>