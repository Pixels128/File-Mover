"""GoogleAuthManager handles google authentication with Flask.

This module initializes the cookies, filesystem, and prepares oauth.
The class itself handles authentication with google. Particuarly, 
loading important information google needs, handling sending the user to google,
and handling when the user returns from google. When the user returns the method
`get_callback_token` returns the token json object back to the main program.

Typical usage example:
    "Example of google_auth_manager"
    # pylint: disable=import-error, no-name-in-module
    from flask import Flask, session, redirect
    from authlib.integrations.flask_client import OAuth
    from flask_session import Session
    import google_auth_manager

    app = Flask(__name__)

    google_auth_manager.initialize(app, Session)
    oauth = google_auth_manager.get_oauth(app, OAuth)


    auth_manager = google_auth_manager.GoogleAuthManager(oauth).load_from_json(
        "client_secret.json"
    )


    @app.route("/signin")
    def signin():
        "Signin page"
        return auth_manager.register({"scope": "openid email profile"})


    @app.route("/callback")
    def callback():
        "Callback page"
        token = auth_manager.get_callback_token()
        session["token"] = token
        return redirect("/welcome")


    app.run()
"""
# pylint: disable=import-error
import json
import os


def initialize(app, session):
    """Initializes the correct filesystem, cookies, etc."""
    app.secret_key = os.urandom(12)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    session(app)


def get_oauth(app, oauth):
    """Get OAuth"""
    return oauth(app)


class GoogleAuthManager:
    """Google authentication manager class"""

    def __init__(self, oauth):
        self.oauth = oauth
        self.google_client_id = None
        self.google_client_secret = None
        self.conf_url = "https://accounts.google.com/.well-known/openid-configuration"

    def load_from_json(self, file):
        """Read the client info from the json file ('client_secret.json') provided by google"""
        with open(file, "r", encoding="utf-8") as f:
            client_dict = json.load(f)
            self.google_client_id = client_dict.get("web").get("client_id")
            self.google_client_secret = client_dict.get("web").get("client_secret")
        return self

    def set_google_client_id(self, client_id):
        """Setter for google client id"""
        self.google_client_id = client_id
        return self

    def set_google_client_secret(self, secret):
        """Setter for google client secret"""
        self.google_client_secret = secret
        return self

    def register(self, client_kwargs):
        """Redirect the user to Google for them to sign into their google account"""
        self.oauth.register(
            name="google",
            client_id=self.google_client_id,
            client_secret=self.google_client_secret,
            server_metadata_url=self.conf_url,
            client_kwargs=client_kwargs,
        )
        redirect_uri = "http://127.0.0.1:5000/callback"
        print(redirect_uri)
        return self.oauth.google.authorize_redirect(redirect_uri)

    def get_callback_token(self):
        """Returns the client token from google after the google signin"""
        return self.oauth.google.authorize_access_token()
