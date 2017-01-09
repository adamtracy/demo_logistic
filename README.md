# demo_logistic
Learning about Flask application server by drawing the Logistic Map.  Some other technologies applied
* D3JS
* spinner.js
* nginx (For EC2)
# Dev client 
## setup
```
# get easy_install
yum install python-setuptools
# base Flask install
easy_install Flask
# numpy had to be installed using yum
yum install numpy
```
## Running
launches the server from the command line on port 5000
```
python ./application.py 
```

# EC2 Installation
## My instance
ssh -i "flask-dev.pem" ec2-user@ec2-54-183-26-194.us-west-1.compute.amazonaws.com


http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/


sudo su -
yum install python-setuptools
easy_install Flask
yum install git
yum install numpy


### https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html
I gave up on this one

### https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/
This seems better, though I did not use the http://gunicorn.org/ front end, instead using the default flask wsgi

#####install nginx
create /etc/yum.repos.d/nginx.repo (adding rhel/7)
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/mainline/rhel/7/$basearch/
gpgcheck=0
enabled=1
then do yum install nginx

cat /var/log/audit/audit.log | grep nginx | grep denied | audit2allow -M mynginx
semodule -i mynginx.pp


# older notes

## did an install of flask api created this project and have learned about flask

decorators used for request handling
templating mechansm
    ->css includes
    ->inheritance

Not much use without a database, so trying out the SQL connection with Sqlalchemy
quickstart: http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application

$ sudo easy_install sqlalchemy
$ sudo easy_install Flask-SQLAlchemy


## OurSQL
 OurSQL does not appear to be simpatico with Flask/SQLAlchemy.  The commit()
 never returns.  I've since reverted to using the basic MySQL connection api
 that comes with python.

 Oursql https://gist.github.com/handloomweaver/1117884

$ export PIP_MYSQL_CONFIG=/usr/local/mysql/bin/mysql_config
$ export MYSQL_CONFIG=/usr/local/mysql/bin/mysql_config
$ pip install oursql

invoke python shell in cwd
$ python

from application import db
you have to do this commit() bs when using an sql server (i guess)
http://stackoverflow.com/questions/13882407/sqlalchemy-blocked-on-dropping-tables

db.session.commit()
db.create_all()




## testing sqlalchemy from console
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


