self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('hisabak-store-v1').then((cache) => {
      return cache.addAll([
        'index.html',
        'items.html',
        'stores.html',
        'settings_menu.html',
        'customers.html',
        'suppliers.html'
      ]);
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
