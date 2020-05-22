'use strict';

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
  .replace(/\-/g, '+')
  .replace(/_/g, '/');
  
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

var applicationServerPublicKey = null
var serverURL = null

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');
  console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);
  
  const title = 'X Æ A-12';
  const options = {
    body: event.data.text(),
    icon: 'static/images/favicon_192.png',
    badge: 'static/images/bell.png'
  };
  
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
  console.log('[Service Worker] Notification click Received.');
  
  event.notification.close();
  
  if (serverURL) {
    event.waitUntil(
      clients.openWindow(serverURL)
    );
  }
});
  
self.addEventListener('pushsubscriptionchange', function(event) {
    console.log('[Service Worker]: \'pushsubscriptionchange\' event fired.');
    const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
    event.waitUntil(
      self.registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey
      })
      .then(function(newSubscription) {
        // TODO: Send to application server
        console.log('[Service Worker] New subscription: ', newSubscription);
      })
  );
});

self.addEventListener("message", function(event) {
  const message = JSON.parse(event.data);
  const type = message.type;
  if (type === 'PUBLIC_PUSH_KEY') {
    applicationServerPublicKey = message.key;
    console.log('[Service Worker]: Registered public server key - ' + applicationServerPublicKey)
  } else if (type === 'SERVER_URL') {
    serverURL = message.key;
    console.log('[Service Worker]: Registered server URL - ' + serverURL)
  } else {
    console.error('[Service Worker]: Unknown message type: ' + type);
  }
}, false);
