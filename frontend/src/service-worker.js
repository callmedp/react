// We won't use precaching
const ignored = self.__WB_MANIFEST;
let denyList = [
  '/logout/',
  '/login/'
]

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
        maxAgeSeconds: 7*24*3600,
        maxEntries: 10
      })
    ]
  })
)



workbox.routing.registerRoute(
  ({ request, url}) => {
    return request.mode === 'navigate' && !denyList.includes(url.pathname);
  },
  new workbox.strategies.NetworkFirst({
    cacheName: 'navigation', 
    plugins: [
     new workbox.expiration.Plugin({
      maxEntries: 20
    })
    ]
  })
  )

workbox.routing.registerRoute(
  ({ request, url}) => {
    return request.mode === 'navigate' && url.pathname == '/logout/';
  },
  async ({request}) => {
    await caches.keys().then(cacheNames => {
      cacheNames.forEach( cacheName => {
        caches.delete(cacheName);
      })
    })
    const response = await fetch(request);
    return response;
  }
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
new workbox.strategies.NetworkFirst({
  cacheName: 'apis',
})
);
