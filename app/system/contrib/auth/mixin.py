import base64
import cgi
import logging
import urllib
import tornado.web
import tornado.auth
from tornado import httpclient
from tornado import escape


class DropboxMixin(tornado.auth.OAuthMixin):
    """ Dropbox  OAuth authentication.
    """
    _OAUTH_REQUEST_TOKEN_URL = "https://api.dropbox.com/1/oauth/request_token"
    _OAUTH_ACCESS_TOKEN_URL = "https://api.dropbox.com/1/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "https://www.dropbox.com/1/oauth/authorize"
    _OAUTH_VERSION = "1.0"
    _OAUTH_NO_CALLBACKS = False

    def authorize_redirect(self, callback_uri=None, extra_params=None,
                           http_client=None):
        """Redirects the user to obtain OAuth authorization for this service.

        Twitter and FriendFeed both require that you register a Callback
        URL with your application. You should call this method to log the
        user in, and then call get_authenticated_user() in the handler
        you registered as your Callback URL to complete the authorization
        process.

        This method sets a cookie called _oauth_request_token which is
        subsequently used (and cleared) in get_authenticated_user for
        security purposes.
        """
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(
            self._oauth_request_token_url(), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHORIZE_URL, callback_uri))

    def get_authenticated_user(self, callback, http_client=None):
        """Gets the OAuth authorized user and access token on callback.

        This method should be called from the handler for your registered
        OAuth Callback URL to complete the registration process. We call
        callback with the authenticated user, which in addition to standard
        attributes like 'name' includes the 'access_key' attribute, which
        contains the OAuth access you can use to make authorized requests
        to this service on behalf of the user.

        """
        request_key = escape.utf8(self.get_argument("oauth_token"))
        oauth_verifier = self.get_argument("oauth_verifier", None)
        request_cookie = self.get_cookie("_oauth_request_token")
        if not request_cookie:
            logging.warning("Missing OAuth request token cookie")
            callback(None)
            return
        self.clear_cookie("_oauth_request_token")
        cookie_key, cookie_secret = [base64.b64decode(escape.utf8(i)) for i in request_cookie.split("|")]
        if cookie_key != request_key:
            logging.info((cookie_key, request_key, request_cookie))
            logging.warning("Request token does not match cookie")
            callback(None)
            return
        token = dict(key=cookie_key, secret=cookie_secret)
        if oauth_verifier:
            token["verifier"] = oauth_verifier
        if http_client is None:
            http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(self._oauth_access_token_url(token),
                          self.async_callback(self._on_access_token, callback))

    def _on_access_token(self, callback, response):
        if response.error:
            logging.warning("Could not fetch access token")
            callback(None)
            return

        access_token = _oauth_parse_response(response.body)
        self._oauth_get_user(access_token, self.async_callback(
             self._on_oauth_get_user, access_token, callback))

    def _on_oauth_get_user(self, access_token, callback, user):
        if not user:
            callback(None)
            return
        user["access_token"] = access_token
        callback(user)

    def dropbox_request(self, path, callback, access_token=None,
                        post_args=None, **args):
        # Add the OAuth resource request signature if we have credentials
        url = "https://api.dropbox.com/1" + path
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args: url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_dropbox_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_dropbox_request(self, callback, response):
        if response.error:
            print("Error response %s fetching %s", response.error,
                            response.request.url)
            callback(None)
            return
        callback(escape.json_decode(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("dropbox_consumer_key", "Dropbox OAuth")
        self.require_setting("dropbox_consumer_secret", "Dropbox OAuth")
        return dict(
            key=self.settings["dropbox_consumer_key"],
            secret=self.settings["dropbox_consumer_secret"])

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        self.dropbox_request(
            "/account/info",
            access_token=access_token,
            callback=callback)

    def _parse_user_response(self, callback, user):
        if user:
            user["username"] = user["display_name"]
        callback(user)


def _oauth_parse_response(body):
    p = escape.parse_qs(body, keep_blank_values=False)
    token = dict(key=p[b("oauth_token")][0], secret=p[b("oauth_token_secret")][0])

    # Add the extra parameters the Provider included to the token
    special = (b("oauth_token"), b("oauth_token_secret"))
    token.update((k, p[k][0]) for k in p if k not in special)
    return token


class LaunchpadMixin(tornado.auth.OAuthMixin, tornado.auth.OpenIdMixin):
    """ launchpad.net oauth
    """
    _OPENID_ENDPOINT = "https://login.launchpad.net"
    _OAUTH_REQUEST_TOKEN_URL = "https://launchpad.net/+request-token"
    _OAUTH_AUTHORIZE_URL = "https://launchpad.net/+authorize-token"
    _OAUTH_ACCESS_TOKEN_URL = "https://launchpad.net/+access-token"
    _OAUTH_NO_CALLBACKS = False
    _OAUTH_SIGNATURE_METHOD = "PLAINTEXT"

    def authorize_redirect(self, callback_uri=None, extra_params=None,
                           http_client=None):
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(
            self._oauth_request_token_url(), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHORIZE_URL, callback_uri))

    def get_authenticated_user(self, callback, http_client=None):
        request_key = escape.utf8(self.get_argument("oauth_token"))
        oauth_verifier = self.get_argument("oauth_verifier", None)
        request_cookie = self.get_cookie("_oauth_request_token")
        if not request_cookie:
            logging.warning("Missing OAuth request token cookie")
            callback(None)
            return
        self.clear_cookie("_oauth_request_token")
        cookie_key, cookie_secret = [base64.b64decode(escape.utf8(i)) for i in request_cookie.split("|")]
        if cookie_key != request_key:
            logging.info((cookie_key, request_key, request_cookie))
            logging.warning("Request token does not match cookie")
            callback(None)
            return
        token = dict(key=cookie_key, secret=cookie_secret)
        if oauth_verifier:
            token["verifier"] = oauth_verifier
        if http_client is None:
            http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(self._oauth_access_token_url(token),
                          self.async_callback(self._on_access_token, callback))

    def _on_access_token(self, callback, response):
        if response.error:
            logging.warning("Could not fetch access token")
            callback(None)
            return

        access_token = _oauth_parse_response(response.body)
        self._oauth_get_user(access_token, self.async_callback(
             self._on_oauth_get_user, access_token, callback))

    def _on_oauth_get_user(self, access_token, callback, user):
        if not user:
            callback(None)
            return
        user["access_token"] = access_token
        callback(user)

    def launchpad_request(self, path, callback, access_token=None,
                        post_args=None, **args):
        # Add the OAuth resource request signature if we have credentials
        url = "https://api.launchpad.net/1.0" + path
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args: url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_dropbox_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_launchpad_request(self, callback, response):
        if response.error:
            print("Error response %s fetching %s", response.error,
                            response.request.url)
            callback(None)
            return
        callback(escape.json_decode(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("launchpad_consumer_key", "Launchpad Application Key")
        return dict(key=self.settings["launchpad_consumer_key"])

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        self.dropbox_request(
            "/account/info",
            access_token=access_token,
            callback=callback)

    def _parse_user_response(self, callback, user):
        if user:
            user["username"] = user["display_name"]
        callback(user)


class GithubMixin(tornado.auth.OAuth2Mixin):
    """ thanks https://github.com/peterbe/tornado_gists/blob/master/apps/main/handlers.py
    """
    _OAUTH_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token?"
    _OAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize?"
    _OAUTH_NO_CALLBACKS = False

    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_fields=None):
        """handles login"""
        http = httpclient.AsyncHTTPClient()
        args = {
          "redirect_uri": redirect_uri,
          "code": code,
          "client_id": client_id,
          "client_secret": client_secret,
        }

        fields = set(['id', 'name', 'first_name', 'last_name',
                      'locale', 'picture', 'link'])
        if extra_fields:
            fields.update(extra_fields)

        url = self._oauth_request_token_url(**args)
        http.fetch(url,
          self.async_callback(self._on_access_token, redirect_uri, client_id,
                              client_secret, callback, fields))

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                        callback, fields, response):
        if response.error:
            logging.warning('Facebook auth error: %s' % str(response))
            callback(None)
            return

        #print "self.request.arguments"
        #print self.request.arguments
        #print "RESPONSE.BODY:"
        #print response.body

        session = {
          "access_token": cgi.parse_qs(response.body)["access_token"][-1],
          "expires": cgi.parse_qs(response.body).get("expires")
        }
        #print "SESSION"
        #print session
        #print "\n"

        self.github_request(
          path="/user/show",
          callback=self.async_callback(
              self._on_get_user_info, callback, session, fields),
          access_token=session["access_token"],
          fields=",".join(fields)
          )

    def _on_get_user_info(self, callback, session, fields, user):
        if user is None:
            callback(None)
            return

        #pprint(user)
        fieldmap = user['user']
        print 'session.get("expires")', repr(session.get("expires"))

        fieldmap.update({"access_token": session["access_token"],
                         "session_expires": session.get("expires")})
        callback(fieldmap)

    def github_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        url = "https://github.com/api/v2/json" + path
        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
            all_args.update(args)
            all_args.update(post_args or {})
        if all_args: url += "?" + urllib.urlencode(all_args)
        callback = self.async_callback(self._on_github_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_github_request(self, callback, response):
        if response.error:
            logging.warning("Error response %s fetching %s", response.error,
                            response.request.url)
            callback(None)
            return
        callback(tornado.escape.json_decode(response.body))
