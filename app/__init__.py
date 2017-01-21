from flask import Flask
from flask.ext.login import LoginManager
from auth import MyAnonymousUser, User
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# OK, I've got issues with this, because the views module has a dependency on this module
# as well.  Explained by this guy:
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# but that seems jacked up, no?
from app import views

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = MyAnonymousUser


@login_manager.user_loader
def load_user(user_id):
    print('user_loader() id={0}'.format(user_id))
    return User(email="", username=user_id, id=user_id)

# Not using the database for this application
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# db = SQLAlchemy(app)


