// Basic no-op service worker for PWA install support

self.addEventListener("install", event => {
  // You could pre-cache assets here later
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  // Cleanup old caches here later if you add caching
  clients.claim();
});

// Minimal fetch handler (required by some browsers)
self.addEventListener("fetch", event => {
  // For now, just let the network handle everything
});
