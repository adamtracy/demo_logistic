from flask import url_for, current_app, redirect, request, session
from rauth import OAuth2Service

import json
import urllib2


class User():
    """
    I'm a basic User class based on Flask's standard, stored in the Http session.
    See: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """
    id = None
    username = None
    email = None
    is_authenticated = False
    is_active = False
    is_anonymous = False

    def __init__(self, username, email, id=None):
        self.username = username
        self.email = email
        self.is_authenticated = True
        self.is_active = True
        self.id = id

    def get_id(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username


class MyAnonymousUser():
    is_active = False
    is_authenticated = False
    username = "Not Logged In"
    is_anonymous = True

    def __init__(self):
        pass

    def get_id(self):
        return self.username

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        print("OAuthSignIn __init__()")

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                        _external=True)
        #return 'http://demo.adamtracystudio.com/callback/google'

    @classmethod
    def get_provider(self, provider_name):
        print('get_provider')
        if self.providers is None:
            self.providers={}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
                print('init {0}'.format(provider.provider_name))
        return self.providers[provider_name]


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urllib2.urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url=google_params.get('authorization_endpoint'),
                base_url=google_params.get('userinfo_endpoint'),
                access_token_url=google_params.get('token_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()
                     },
                decoder = json.loads
        )
        me = oauth_session.get('').json()
        return (me['name'],
                me['email'])
