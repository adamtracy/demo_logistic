from flask import Flask, Response
from flask import render_template

# from flask_sqlalchemy import SQLAlchemy

from logistic import LogisticEquation
import json

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+oursql://adamtracy@localhost/flask_test'
#  for some reason oursql hangs when doing commits on the Session object.  vanilla mysql
# connection does not appear to do so.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adamtracy@localhost/flask_test'

# when using regular sqlalchemy, you interact with the engine directly (i think).
# Flask appears to manage this for you, perhaps for resource management, etc.
#
"""
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
"""

@app.route('/')
def index():
    name = 'Index'
    return render_template('index.html', name=name)


@app.route('/logistic/<float:r_min>/<float:r_max>/<float:x_min>/<float:x_max>')
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

if __name__ == "__main__":
    app.run()
