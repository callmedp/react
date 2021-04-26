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
    cacheName: 'assets',
    plugins: [
      new workbox.expiration.Plugin({
        maxAgeSeconds: 7*24*3600
      })
    ]
  })
)


workbox.routing.registerRoute(
({ request, url}) => {
  console.log("navigation url", url)
  return request.mode === 'navigate';
},
new workbox.strategies.StaleWhileRevalidate({
  cacheName: 'navigation', 
  plugins: [
    new workbox.cacheableResponse.Plugin({
      statuses: [0, 200, 206]  
   }),
   new workbox.expiration.Plugin({
    maxAgeSeconds: 24*3600, 
    maxEntries: 20
  })

  ]
})
)

workbox.routing.registerRoute(
({ url }) => {
  return (url.pathname.endsWith('.jpg') || url.pathname.endsWith('.png') || url.pathname.endsWith('.svg'));
}, 
new workbox.strategies.CacheFirst({
  cacheName: 'images', 
  plugins: [
    new workbox.expiration.Plugin({
      maxAgeSeconds: 30*24*3600, 
      maxEntries: 50
    })
  ]
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
