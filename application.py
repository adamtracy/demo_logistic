from flask import Flask, Response, render_template, redirect, url_for, session, g
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
import json
from logistic import LogisticEquation
from auth import OAuthSignIn, MyAnonymousUser, User
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
GOOGLE_LOGIN_CLIENT_ID = "375083735774-nmnutf79vr2ej5ardierqc5bj2oq9pv0.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "r2E35GWaMhgRGClpR8z5_ljQ"

OAUTH_CREDENTIALS = {
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
}
app.config['OAUTH_CREDENTIALS'] = OAUTH_CREDENTIALS

app.secret_key = 'xxxxyyyyyzzzzz'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = MyAnonymousUser

app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+oursql://adamtracy@localhost/flask_test'
#  for some reason oursql hangs when doing commits on the Session object.  vanilla mysql
# connection does not appear to do so.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adamtracy@localhost/flask_test'

# when using regular sqlalchemy, you interact with the engine directly (i think).
# Flask appears to manage this for you, perhaps for resource management, etc.
#

# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    print('user_loader() id={0}'.format(user_id))
    return User(email="", username=user_id, id=user_id)


@app.before_request
def before_request():
    # as I understand it, g.user has a lifecycle spanning the duration of the request.
    # current_user has the lifecycle of the session into the server (which appears to be
    # stowed in a client side cookie).
    # I see people assign g.user in before_request() like this so that it can be accessed
    # in template code, but i'm not entirely sure why this you don't just use the session
    # current_user directly, though :/
    print('user_loader() id={0}'.format(current_user))
    g.user = current_user


@app.route('/')
def index():
    return render_template('index.html',
                           title='Index',
                           user=g.user)


@app.route('/logistic_equation/')
@login_required
def logistic_equation():
    return render_template('logistic_equation.html',
                           title='Logistic',
                           user=g.user)


@app.route('/logistic/<float:r_min>/<float:r_max>/<float:x_min>/<float:x_max>')
@login_required
def logistic(r_min, r_max, x_min, x_max):
    logistic_eq = LogisticEquation(r_min=r_min,
                                   r_max=r_max,
                                   x_min=x_min,
                                   x_max=x_max)
    logistic_eq.calc()
    resp = Response(response=json.dumps(logistic_eq.plot),
                    status=200,
                    mimetype="application/json")
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In')


@app.route('/logout')
def logout():
    # Remove the user information from the session
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not g.user.is_anonymous:
        print('redirecting?')
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not g.user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))
    # Once we have the user auth creds, we can persist their deets
    # in a local database.  In this case, i'm not going to do it.
    if username is None or username == "":
        username = email.split('@')[0]
    user = User(username=username, email=email)
    print('Logging in: {0} {1}'.format(username, email))
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
