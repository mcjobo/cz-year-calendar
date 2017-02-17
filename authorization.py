
import requests
import jwt
import cherrypy
import os
import hashlib
from configobj import ConfigObj

redirect = "http://localhost:8080/redirect"
config = ConfigObj("year/settings.ini")

def check_authorized():
    session = cherrypy.session
    if 'ident' not in session:
        ident = hashlib.sha256(os.urandom(1024)).hexdigest()
        cherrypy.session["ident"] = ident
    print("session", session["ident"])
    if "user" not in session:
        raise cherrypy.HTTPError(401)
    return "user" in session
    # return False


def get_authorization_url(provider):
    doc = get_discovery_document(provider)
    url = doc["authorization_endpoint"] + "?"
    url += "client_id=" + get_client_id(provider)
    url += "&response_type=" + "code"
    url += "&redirect_uri=" + redirect
    url += "&scope=" + "openid%20email"
    url += "&state=" + cherrypy.session["ident"]
    if "loginhint" in cherrypy.request.cookie:
        print("loginhint", cherrypy.request.cookie.keys())
        print("loginhint2", cherrypy.request.cookie["loginhint"])
        url += "&login_hint=" + str(cherrypy.request.cookie["loginhint"])
    return url

def get_discovery_document(provider):
    return get_google_discovery_document();


def get_google_discovery_document():
    r = requests.get('https://accounts.google.com/.well-known/openid-configuration')
    return r.json()


def get_client_id(provider):
    return "11857317883-k4a5caf0mgo5ivthe61gr4gs437m88jm.apps.googleusercontent.com"


def get_client_secret(provider):
    return "zSvVjrL9uIW0lxgO3SaxtyFN"


def validate_state_token(params):
    print("state token: ", params["state"], cherrypy.session["ident"])
    if params["state"] != cherrypy.session["ident"]:
        raise cherrypy.HTTPError(403)


def exchange_authorization_token(provider, params):
    url = get_discovery_document(provider)["token_endpoint"]
    url += "?code=" + params["code"]
    url += "&client_id=" + get_client_id(provider)
    url += "&client_secret=" + get_client_secret(provider)
    url += "&redirect_uri=" + redirect
    url += "&grant_type=" + "authorization_code"
    token = requests.post(url).json()
    print("result", token)
    jwt = decode_id_token(token["id_token"])
    if authorize_user(jwt["email"]):
        print("authorized")
        cherrypy.session["user"] = jwt["email"]
        cherrypy.response.cookie["loginhint"] = jwt["email"]


def decode_id_token(id_token):
    jwebtoken = jwt.decode(id_token, verify=False)
    print("jwttoken: ", jwebtoken)
    return jwebtoken

def authorize_user(useremail):
    print("authorized", useremail, config["authorization"]["user_mails"])
    return True if useremail in config["authorization"]["user_mails"] else False