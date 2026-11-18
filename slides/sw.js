// Keeps slideshow media on the TV so each loop plays from local storage, not the internet.
// Media files are cache-first (rename a file to replace it). Everything else is network-first.
var CACHE = 'acr-slides-media-v2';
self.addEventListener('install', function(e){ self.skipWaiting(); });
self.addEventListener('activate', function(e){ e.waitUntil(caches.keys().then(function(ks){ return Promise.all(ks.filter(function(k){ return k !== CACHE; }).map(function(k){ return caches.delete(k); })); }).then(function(){ return self.clients.claim(); })); });
self.addEventListener('fetch', function(e){
  var url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (url.pathname.indexOf('/slides/media/') !== -1) {
    // Video range requests: serve whole cached file; browsers handle a full 200 response fine.
    e.respondWith(caches.open(CACHE).then(function(c){
      return c.match(url.pathname).then(function(hit){
        if (hit) return hit;
        return fetch(url.pathname).then(function(r){ if (r.ok && r.status === 200) c.put(url.pathname, r.clone()); return r; });
      });
    }));
  }
});
