const READWAVE_CACHE = "readwave-shell-v93";
const SHELL_ASSETS = [
  "/",
  "/assets/styles.css?v=20260425palette13",
  "/assets/app.js?v=20260425palette13",
  "/assets/readwave-icon.svg",
  "/assets/readwave-favicon.png",
  "/assets/readwave-logo.png",
  "/assets/readwave-mark.png",
  "/assets/readwave-icon-180.png",
  "/assets/readwave-icon-192.png",
  "/assets/readwave-icon-512.png",
  "/manifest.webmanifest"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(READWAVE_CACHE).then((cache) => cache.addAll(SHELL_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== READWAVE_CACHE).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith("/api/") || event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const clone = response.clone();
        caches.open(READWAVE_CACHE).then((cache) => cache.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request).then((cached) => cached || caches.match("/")))
  );
});
