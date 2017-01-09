# demo_logistic
getting used to flask application server, d3 rendition of Logistic Equation




###################
### older notes ###
###################

did an install of flask api created this project and have learned about flask

decorators used for request handling
templating mechansm
    ->css includes
    ->inheritance

Not much use without a database, so trying out the SQL connection with Sqlalchemy
quickstart: http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application

$ sudo easy_install sqlalchemy
$ sudo easy_install Flask-SQLAlchemy

##
## OurSQL
##
# OurSQL does not appear to be simpatico with Flask/SQLAlchemy.  The commit()
# never returns.  I've since reverted to using the basic MySQL connection api
# that comes with python.
#
# Oursql https://gist.github.com/handloomweaver/1117884

$ export PIP_MYSQL_CONFIG=/usr/local/mysql/bin/mysql_config
$ export MYSQL_CONFIG=/usr/local/mysql/bin/mysql_config
$ pip install oursql

invoke python shell in cwd
$ python

from application import db
# you have to do this commit() bs when using an sql server (i guess)
# http://stackoverflow.com/questions/13882407/sqlalchemy-blocked-on-dropping-tables

db.session.commit()
db.create_all()



###
### testing sqlalchemy from console
###
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://adamtracy@localhost/flask_test')

Session = sessionmaker(bind=engine)
session=Session()
from application import User
admin=User('admin','foo@boo.com')
session.add(admin)
session.commit()


from application import User
admin = User('admin', 'admin@example.com')


