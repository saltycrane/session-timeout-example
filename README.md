### Bank style session timeout example

This is an example that uses Javascript to display a session timeout
warning modal 10 minutes before session expiration. It also resets the
session expiration whenever the user clicks the mouse. It uses
Javascript, jQuery, and Boostrap on the frontend and Python, Flask,
Flask-Login, and WTForms on the backend.

 - Mouse clicks anywhere on the page ping the server at a maximum
   frequecy of once per minute and reset the session expiration.
 - 10 minutes before the session expiration, a warning modal is
   displayed with two buttons: "Log out" and "Stay Logged In".
 - If the user clicks "Stay Logged In" the session expiration is reset.
 - If the user clicks "Log out", the user is logged out.
 - If the user does nothing for 10 minutes, the user is logged out and
   displayed a message that the session timed out.

The code:

The meat of the code is in [`static/session-monitor.js`](https://github.com/saltycrane/session-timeout-example/blob/master/static/session-monitor.js)

Usage:

 - Set up and run the server
 
        $ virtualenv venv
        $ source venv/bin/activate
        $ pip install -r requirements.txt
        $ python myapp.py

 - Go to http://127.0.0.1:5000/ in the browser.
 - Enter george for the username and george for the password.
 - Click the mouse to prolong the session.
 - Wait several seconds for the warning modal to show up.
 - Click "Stay Logged In" to stay logged in or do nothing to automatically be logged out.

Notes:

 - I set very small timeout values set (i.e. a few seconds) for demo
   purposes only. In a real application, set them to larger values in
   the range of minutes to hours.
 - I know Python better than Javascript.
