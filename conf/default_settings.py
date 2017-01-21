# Google keys managed here:
# https://console.developers.google.com/apis/credentials?project=teak-strength-156021
GOOGLE_LOGIN_CLIENT_ID = "375083735774-6qk0691sblasfhujmc5l6pglgpdldnvp.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "J66Qh4Eii7OZglH3EKc3Fghu"

OAUTH_CREDENTIALS = {
    'google': {
        'id': GOOGLE_LOGIN_CLIENT_ID,
        'secret': GOOGLE_LOGIN_CLIENT_SECRET
    }
}

OAUTH_CREDENTIALS = OAUTH_CREDENTIALS
DEBUG = True
SECRET_KEY = 'xxxxyyyyyzzzzz'

# SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
# SQLALCHEMY_DATABASE_URI = 'mysql+oursql://adamtracy@localhost/flask_test'
#  for some reason oursql hangs when doing commits on the Session object.  vanilla mysql
# connection does not appear to do so.
SQLALCHEMY_DATABASE_URI = 'mysql://adamtracy@localhost/flask_test'

