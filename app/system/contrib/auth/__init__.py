import traceback
import tornado.web
from app.system.contrib.util import hash_login
from app.system.handler import BaseHandler
from app.system.contrib.auth import mixin
from app.system.log import logger as watchdog
from app.models.schema import Client

class LoginHandler(BaseHandler):
    def get(self):
        """ Override this method to provide a login form """
        pass

    def post(self):
        login_hash = hash_login(self.get_argument("username"),
                                self.get_argument("password"))
        user = self.session.query(Client).filter(Client.username==self.get_argument("username"),
                                                 Client.password==login_hash).one()
        if user:
            watchdog.debug('Found %s' % (user.username,))
            self.set_secure_cookie("userid", str(user.id))
            if user.is_staff:
                self.set_secure_cookie("is_staff", "1")
            self.set_secure_cookie("username", user.username)
            self.send_statmsg("Logged in successfully.")
            self.redirect(self.get_argument("next") if \
                              self.is_argument_present("next") else "/")
        else:
            self.send_errmsg("Login incorrect")
            self.redirect("/auth/login")

class LogoutHandler(BaseHandler):
    def get(self):
        pass

class RegisterHandler(BaseHandler):
    def get(self):
        """ Override with register template """
        pass

    def post(self):
        """ Override with post template """
        try:
            if not (self.validate_passwords()):
                self.send_errmsg("Passwords empty/do not match")
                self.redirect("/auth/register")
            login_hash = hash_login(self.get_argument("username"),
                                    self.get_argument("password"))

            self.redirect("/auth/login")
        except:
            self.send_errmsg("Registration failed: \n%s" % traceback.format_exc())
            self.redirect("/auth/register")


class GithubLoginHandler(BaseHandler, mixin.GithubMixin):
    """ thanks https://github.com/peterbe/tornado_gists/blob/master/apps/main/handlers.py
    """
    @tornado.web.asynchronous
    def get(self):
        settings_ = settings.OAUTH_SETTINGS
        if self.get_argument("code", False):
            self.get_authenticated_user(
                  redirect_uri=settings_['redirect_url'],
                  client_id=settings_['client_id'],
                  client_secret=settings_['client_secret'],
                  code=self.get_argument("code"),
                  callback=self.async_callback(
                    self._on_login))
            return

        self.authorize_redirect(redirect_uri=settings_['redirect_url'],
                                client_id=settings_['client_id'],
                                extra_params={})#"scope": "read_stream,offline_access"})

    def _on_login(self, github_user):
        if not github_user.get('login'):
            return self.redirect('/?login_failed=true')

        """ db github
        user = self.db.User.one({'login':unicode(github_user['login'])})
        if user is None:
            user = self.db.User()
            user.login = unicode(github_user['login'])
            #print "CREATE NEW USER"
        for key in ('email', 'name', 'company', 'gravatar_id', 'access_token'):
            if key in github_user:
                value = github_user[key]
                if value is not None:
                    setattr(user, key, unicode(value))
        user.save()
        self.set_secure_cookie("user", str(user._id), expires_days=100)
        """

        self.redirect('/')
