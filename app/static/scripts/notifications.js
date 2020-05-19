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

function updateSubscriptionOnServer(subscription) {
    if (subscription) {
        const subscriptionJSON = JSON.stringify(subscription);
        console.log('Sending to server notification subscription update: ' + subscriptionJSON);
        const payload = new URLSearchParams();
        payload.append('csrf_token', getCSRFToken())
        payload.append('subscription', subscriptionJSON)
        return fetch(`${window.location.protocol}//${window.location.host}/subscribe`, {
            method: 'POST',
            body: payload
        })
    } else {
        console.log('Sending to server notification subscription update: No subscription');
        const payload = new URLSearchParams();
        payload.append('csrf_token', getCSRFToken())
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
            console.log('User is subscribed.');

            updateSubscriptionOnServer(subscription);

            isSubscribed = true;

            updateBtn();
        })
        .catch(function (err) {
            console.log('Failed to subscribe the user: ', err);
            updateBtn();
        });
}

function unsubscribeUser() {
    swRegistration.pushManager.getSubscription()
        .then(function (subscription) {
            if (subscription) {
                return subscription.unsubscribe();
            }
        })
        .catch(function (error) {
            console.log('Error unsubscribing', error);
        })
        .then(function () {
            updateSubscriptionOnServer(null);

            console.log('User is unsubscribed.');
            isSubscribed = false;

            updateBtn();
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
            isSubscribed = !(subscription === null);

            updateSubscriptionOnServer(subscription);

            if (isSubscribed) {
                console.log('User IS subscribed.');
            } else {
                console.log('User is NOT subscribed.');
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