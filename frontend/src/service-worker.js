// We won't use precaching
const ignored = self.__WB_MANIFEST;

self.addEventListener('install',(event) => {
  caches.keys().then(cacheNames => {
    cacheNames.forEach( cacheName => {
      caches.delete(cacheName);
    })
  })
  self.skipWaiting()
}
)


workbox.routing.registerRoute(
  /\.(?:js|css)$/,
  new workbox.strategies.CacheFirst({
    cacheName: 'assets'
  })
)


workbox.routing.registerRoute(
({ request, url}) => {
 
  return request.mode === 'navigate';
},
new workbox.strategies.StaleWhileRevalidate({
  cacheName: 'navigation'
})
)

workbox.routing.registerRoute(
({ url }) => {
  return url.origin === self.location.origin && (url.pathname.endsWith('.jpg') || url.pathname.endsWith('.png') || url.pathname.endsWith('.svg'));
}, 
new workbox.strategies.CacheFirst({
  cacheName: 'images'
})
)

workbox.routing.registerRoute(
({ url, request }) => {
    return url.origin === self.location.origin && request.mode !== 'navigate';
},
new workbox.strategies.StaleWhileRevalidate({
  cacheName: 'apis',
})
);


