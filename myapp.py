import collections
import datetime

from flask import Flask, request, render_template, redirect, url_for, session
from flask.ext.login import (
    LoginManager, login_user, logout_user,  UserMixin, login_required)
from wtforms.fields import PasswordField, StringField
from wtforms.form import Form


UserRow = collections.namedtuple('UserRow', ['id', 'password'])
TOY_USER_DATABASE = {
    'george': UserRow(id=1, password='george'),
}


# settings ###############################################################
# Set a secret key to sign the session (Flask config value)
SECRET_KEY = 'insert secret key here'

# The amount of time after which the user's session expires
# (this is a Flask setting and is also used by the Javascript)
PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=60)


# init ###############################################################
app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '.login'


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.context_processor
def add_session_config():
    """Add current_app.permanent_session_lifetime converted to milliseconds
    to context. The config variable PERMANENT_SESSION_LIFETIME is not
    used because it could be either a timedelta object or an integer
    representing seconds.
    """
    return {
        'PERMANENT_SESSION_LIFETIME_MS': (
            app.permanent_session_lifetime.seconds * 1000),
    }


# models ###############################################################
class User(UserMixin):
    def __init__(self, id):
        self.id = id


# forms ###############################################################
class LoginForm(Form):
    username = StringField()
    password = PasswordField()


# views ###############################################################
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    message = ''

    if request.method == 'POST' and form.validate():
        db_user = TOY_USER_DATABASE.get(form.username.data)
        if form.password.data == db_user.password:
            user = User(db_user.id)
            login_user(user)
            return redirect(url_for('.home'))
        else:
            message = 'Login failed.'

    context = {
        'form': form,
        'message': message,
    }
    return render_template('login.html', **context)


@app.route("/")
@login_required
def home():
    return render_template('home.html')


@app.route("/another-page")
@login_required
def another_page():
    return render_template('another_page.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.logged_out') + '?' + request.query_string)


@app.route("/logged-out")
def logged_out():
    timed_out = request.args.get('timeout')
    return render_template('logged_out.html', timed_out=timed_out)


@app.route("/ping", methods=['POST'])
def ping():
    session.modified = True
    return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
