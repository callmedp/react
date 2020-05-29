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
  "https://learning-static-staging-189607.storage.googleapis.com/l1/s/score-checker/dist/desktop/precache-manifest.a41e038772873f845d3d920eaa1379af.js"
=======
  "https://learning-static-staging-189607.storage.googleapis.com/l1/s/score-checker/dist/desktop/precache-manifest.64aa2850104ce989b77d5123c09ffb7f.js"
>>>>>>> fixed: candidate_id issue fixed
=======
  "https://learning-static-staging-189607.storage.googleapis.com/l1/s/score-checker/dist/desktop/precache-manifest.e789678c2fd43bf8e62c6b4852deeb05.js"
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
