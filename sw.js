// Updated 1790789687.8868246
// Updated 1790790837.1800249
// Settings 1790794024.4476008
// SettingsMenu 1790799736.0429056
// HubReady 1790799789.055942
const CACHE_NAME = "hisabak-v" + Date.now();
self.addEventListener("install", (e) => {
  self.skipWaiting();
});
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(keys.map((k) => caches.delete(k)));
    }).then(() => self.clients.claim())
  );
});
self.addEventListener("fetch", (e) => {
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});