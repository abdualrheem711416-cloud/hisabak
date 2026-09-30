// CacheUpdate_1790800830\n// Fix404_1790801269\n// ThemedVoucher_1790802393\nconst CACHE_NAME = 'hisabak-cache-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './invoice.html',
  './customers.html',
  './suppliers.html',
  './settings.html',
  './settings_menu.html',\n  './vouchers.html',\n  './invoices_list.html',\n  './statement.html',
  './manifest.json',
  './icon-512.png'
];

// 1. عند تثبيت الخدمة: تحميل وتخزين جميع الملفات مسبقاً
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// 2. عند التفعيل: حذف النسخ القديمة واستلام التحكم فوراً
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. عند طلب أي صفحة: محاولة الشبكة، وإن انقطع الإنترنت العودة فوراً للكاش
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // تحديث الكاش بالنسخة الأحدث في الخلفية
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(async () => {
        // إذا انقطع الإنترنت: جلب الملف المطابق من الكاش
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) {
          return cachedResponse;
        }

        // إذا كان الطلب لصفحة HTML ولم يجدها مباشرة (مثل الروابط مع معلمات)، يعرض index.html
        if (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) {
          const url = new URL(event.request.url);
          const pathname = url.pathname.split('/').pop() || 'index.html';
          return caches.match('./' + pathname).then(res => res || caches.match('./index.html'));
        }
      })
  );
});
