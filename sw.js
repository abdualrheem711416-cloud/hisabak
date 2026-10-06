const CACHE_NAME = 'hisabak-v2026-offline-v2';

const APP_FILES = [
  './',
  './index.html',
  './invoice.html',
  './invoices_list.html',
  './vouchers.html',
  './statement.html',
  './customers.html',
  './suppliers.html',
  './items.html',
  './stores.html',
  './currencies.html',
  './settings.html',
  './settings_menu.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',

  './core/storage.js',
  './core/accounting.js',
  './core/inventory.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {
      await Promise.allSettled(
        APP_FILES.map(file => cache.add(file))
      );
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;

  if (request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(request)
      .then(response => {
        if (
          response &&
          response.status === 200 &&
          response.type === 'basic'
        ) {
          const copy = response.clone();

          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, copy);
          });
        }

        return response;
      })
      .catch(() =>
        caches.match(request).then(cached => {
          if (cached) {
            return cached;
          }

          if (request.mode === 'navigate') {
            return caches.match('./index.html');
          }

          return new Response('', {
            status: 503,
            statusText: 'Offline'
          });
        })
      )
  );
});
