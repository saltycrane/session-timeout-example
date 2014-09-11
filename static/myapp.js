$(document).ready(function() {

    window.SessionMonitor = function() {
        // Ideas from http://www.itworld.com/development/335546/how-create-session-timeout-warning-your-web-application-using-jquery

        "use strict";

        var MIN_PING_INTERVAL_MS = window.myapp.MIN_PING_INTERVAL_MS,
            // Subtract MIN_PING_INTERVAL to ensure the backend does not expire the session before this code does.
            EXPIRATION_TIME_MS = window.myapp.PERMANENT_SESSION_LIFETIME_MS - MIN_PING_INTERVAL_MS,
            WARNING_TIME_MS = EXPIRATION_TIME_MS - window.myapp.TIME_BEFORE_WARNING_MS,

            warningIsDisplayed = false,
            // The time of the last ping to the server
            lastPing = 0,
            warningTimeoutID,
            expirationTimeoutID,

            init = function() {
                $("#session-warning-modal").modal({
                    "backdrop": "static",
                    "show": false
                });
                // Ensure that inner elements do not have "mouseup" event handlers that stop propagation.
                $(document).on('mouseup', userDidSomething);
                $("#session-warning-modal").on("click", "#stay-logged-in", stayLoggedInClicked);
                $("#session-warning-modal").on("click", "#log-out", logOutClicked);

                userDidSomething();
            },
            stayLoggedInClicked = function(e) {
                warningIsDisplayed = false;
                userDidSomething();
            },
            logOutClicked = function(e) {
                window.location.href = '/logout';
            },
            userDidSomething = function(e) {
                var now,
                    timeSinceLastPing;

                if (!warningIsDisplayed) {
                    now = new Date();
                    timeSinceLastPing = now - lastPing;

                    if (timeSinceLastPing > MIN_PING_INTERVAL_MS) {
                        lastPing = now;
                        resetTimers();
                        pingServer();
                    }
                }
            },
            resetTimers = function() {
                clearTimeout(warningTimeoutID);
                clearTimeout(expirationTimeoutID);
                warningTimeoutID = setTimeout(displayWarning, WARNING_TIME_MS);
                expirationTimeoutID = setTimeout(logOutByTimeout, EXPIRATION_TIME_MS);
            },
            pingServer = function() {
                $.ajax({
                    type: 'POST',
                    url: '/ping'
                });
            },
            displayWarning = function() {
                warningIsDisplayed = true;
                $("#session-warning-modal").modal("show");
            },
            logOutByTimeout = function() {
                window.location.href = '/logout?sessionTimeout=1';
            };

        return {
            "init": init
        };
    }();

    window.SessionMonitor.init();
});
