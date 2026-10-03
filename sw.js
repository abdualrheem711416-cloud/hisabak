const CACHE_NAME = 'hisabak-v2026-pro';
const urlsToCache = [
  'index.html',
  'currencies.html',
  'settings_menu.html',
  'items.html',
  'stores.html',
  'customers.html',
  'suppliers.html',
  'statement.html',
  'vouchers.html',
  'manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        return response || fetch(event.request).catch(() => {
          if (event.request.mode === 'navigate') {
            return caches.match('index.html');
          }
        });
      })
  );
});
