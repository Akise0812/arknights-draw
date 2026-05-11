// Service Worker - 简单的离线缓存
const CACHE_NAME = 'arknights-pwa-v1';

// 需要预缓存的静态资源（你可以按需添加）
const PRE_CACHE_URLS = [
  '/',
  '/manifest.json'
];

// 安装事件：预缓存关键文件
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRE_CACHE_URLS);
    })
  );
  // 强制新 Service Worker 立即激活
  self.skipWaiting();
});

// 激活事件：清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME).map(name => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// 请求拦截：优先使用缓存，网络失败时回退到缓存
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      return cachedResponse || fetch(event.request).catch(() => {
        // 如果请求的是页面，可以返回默认的离线页面（可选）
        return new Response('当前处于离线状态，请连接网络后重试');
      });
    })
  );
});
