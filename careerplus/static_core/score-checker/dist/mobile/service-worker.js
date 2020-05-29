/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

importScripts(
<<<<<<< HEAD
<<<<<<< HEAD
  "https://learning-static-staging-189607.storage.googleapis.com/l1/s/score-checker/dist/mobile/precache-manifest.b96a0212c79c8a7abc52d98a91916ebc.js"
=======
  "https://learning-static-staging-189607.storage.googleapis.com/l1/s/score-checker/dist/mobile/precache-manifest.3cde09c86493025f585841ace7864feb.js"
>>>>>>> fixed: candidate_id issue fixed
=======
  "https://learning-static-staging-189607.storage.googleapis.com/l1/s/score-checker/dist/mobile/precache-manifest.2c9e01e524ab7d36fa87e906f675d73d.js"
>>>>>>> fixed: candidate_id issue fixed
);

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

workbox.core.clientsClaim();

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

workbox.routing.registerNavigationRoute(workbox.precaching.getCacheKeyForURL("/index.html"), {
  
  blacklist: [/^\/_/,/\/[^\/?]+\.[^\/]+$/],
});
