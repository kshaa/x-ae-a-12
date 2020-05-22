'use strict';

const pushButton = document.querySelector('.js-push-btn');

let isSubscribed = false;
let swRegistration = null;

function getCSRFToken() {
    return document.getElementById('csrf_token').value
}

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

function buttonState(newState) {
    const knownStates = [
        'unsupported',
        'enabled',
        'blocked',
        'loading',
        'available',
        'error'
    ];
    if (!pushButton) {
        console.log('Push button not available, notification management disabled');
        return;
    }
    for (let state of knownStates) {
        pushButton.classList.remove(state)
    }
    if (knownStates.includes(newState)) {
        pushButton.classList.add(newState)
    } else {
        pushButton.classList.add('error')
    }
}
function updateBtn() {
    if (Notification.permission === 'denied') {
        buttonState('blocked');
        updateSubscriptionOnServer(null);
        return;
    }

    if (isSubscribed) {
        buttonState('enabled');
    } else {
        buttonState('available');
    }
}

function updateSubscriptionOnServer(subscription, shouldBeSubscribed) {
    if (!subscription) {
        console.erro("Trying to update a non-existant subscription on server")
    }

    const subscriptionJSON = JSON.stringify(subscription);
    if (shouldBeSubscribed) {
        console.log('Sending to server subscription: ' + subscriptionJSON);
        const payload = new URLSearchParams();
        payload.append('csrf_token', getCSRFToken())
        payload.append('subscription', subscriptionJSON)
        return fetch(`${window.location.protocol}//${window.location.host}/subscribe`, {
            method: 'POST',
            body: payload
        })
    } else {
        console.log('Sending to server unsubscription: ' + subscriptionJSON);
        const payload = new URLSearchParams();
        payload.append('csrf_token', getCSRFToken())
        payload.append('subscription', subscriptionJSON)
        return fetch(`${window.location.protocol}//${window.location.host}/unsubscribe`, {
            method: 'POST',
            body: payload
        })
    }
}

function subscribeUser() {
    const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
    swRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey
    })
        .then(function (subscription) {
            console.log('Subscribed user');

            updateSubscriptionOnServer(subscription, true);
            isSubscribed = true;

            updateBtn();
        })
        .catch(function (err) {
            console.log('Failed to subscribe user: ', err);
            updateBtn();
        });
}

function unsubscribeUser() {
    swRegistration.pushManager.getSubscription()
        .then(function(subscription) {
            if (subscription) {
                subscription.unsubscribe();
            }

            return subscription
        })
        .then(function(subscription) {
            if (subscription) {
                updateSubscriptionOnServer(subscription, false);
            }
            
            console.log('Unsubscribed user');
            isSubscribed = false;
            
            updateBtn();
        })
        .catch(function(error) {
            console.log('Failed to unsubscribe user:', error);
        });
}

function initializeUI() {
    if (!pushButton) {
        console.log('Push button not available, notification management disabled');
        return;
    }
    pushButton.addEventListener('click', function () {
        buttonState('loading');

        if (isSubscribed) {
            unsubscribeUser();
        } else {
            subscribeUser();
        }
    });

    // Set the initial subscription value
    swRegistration.pushManager.getSubscription()
        .then(function (subscription) {
            isSubscribed = subscription !== null;

            if (isSubscribed) {
                updateSubscriptionOnServer(subscription, true);
                console.log('User is subscribed');
            } else {
                console.log('User is unsubscribed');
            }

            updateBtn();
        });
}

function getServerPublicKey() {
    if (typeof applicationServerPublicKey === 'undefined') {
        return null
    }
    if (applicationServerPublicKey === '') {
        return null
    }
    return applicationServerPublicKey
}

function getServerURL() {
    if (typeof applicationServerURL === 'undefined') {
        return null
    }
    if (applicationServerURL === '') {
        return null
    }
    return applicationServerURL
}

if (!getServerPublicKey()) {
    console.error('Server public notification key not defined, notification management disabled');
    buttonState('error');
}

if (getServerPublicKey() && 'serviceWorker' in navigator && 'PushManager' in window) {
    console.log('Push notifications supported')
    buttonState('available');

    navigator.serviceWorker
        .register('/sw.js')
        .then(function (swReg) {
            console.log('Service Worker is registered', swReg);
            swRegistration = swReg;
            return navigator.serviceWorker.ready;
        })
        .then(function () {
            console.log('Service Worker is active');
            swRegistration.active.postMessage(JSON.stringify({
                type: 'PUBLIC_PUSH_KEY',
                key: getServerPublicKey()
            }))
            swRegistration.active.postMessage(JSON.stringify({
                type: 'SERVER_URL',
                key: getServerURL()
            }))
            initializeUI();
        })
        .catch(function (error) {
            console.error('Service Worker Error', error);
            buttonState('error');
        });
} else {
    console.log('Push notifications not supported')
    buttonState('unsupported');
}