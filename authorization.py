
import requests
import jwt
import cherrypy
import os
import hashlib
import json
from configobj import ConfigObj

# redirect = cherrypy.url() + "/calendar/redirect"
# redirect = "http://localhost:8080" "/calendar/redirect"
config = ConfigObj("year/settings.ini")

def check_authorized():
    cookie = {} if "calendar"  not in cherrypy.request.cookie else json.loads(cherrypy.request.cookie["calendar"].value)
    if 'ident' not in cookie:
        ident = hashlib.sha256(os.urandom(1024)).hexdigest()
        cookie["ident"] = ident
        #cherrypy.response.cookie["calendar"] = json.dumps(cookie)

        realCookie = cherrypy.response.cookie
        realCookie["calendar"] = json.dumps(cookie)
        realCookie["calendar"]["path"] = "/"

        print("created new ident key")
    # print("cookie", cherrypy.request.cookie["ident"])
    if "user" not in cookie:
        raise cherrypy.HTTPError(401)
    return "user" in cookie
    # return False


def get_authorization_url(provider):
    application = cherrypy.tree.apps['/calendar']
    redirect = application.config['global']['redirect']
    cookie = json.loads(cherrypy.request.cookie["calendar"].value)
    print("redirect url: ", redirect, cookie, cherrypy.url() + "/calendar/redirect")
    doc = get_discovery_document(provider)
    url = doc["authorization_endpoint"] + "?"
    url += "client_id=" + get_client_id(provider)
    url += "&response_type=" + "code"
    url += "&redirect_uri=" + redirect
    url += "&scope=" + "openid%20email"
    url += "&state=" + cookie["ident"]
    if "loginhint" in cookie:
        print("loginhint", cookie["loginhint"])
        url += "&login_hint=" + str(cookie["loginhint"])
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
    cookie = json.loads(cherrypy.request.cookie["calendar"].value)
    print("state token: ", params["state"], cookie)
    if params["state"] != cookie["ident"]:
        raise cherrypy.HTTPError(403)


def exchange_authorization_token(provider, params):
    application = cherrypy.tree.apps['/calendar']
    redirect = application.config['global']['redirect']
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
        print("authorized", jwt["email"])
        cookie = json.loads(cherrypy.request.cookie["calendar"].value)
        cookie["user"] = jwt["email"]
        cookie["loginhint"] = jwt["email"]

        realCookie = cherrypy.response.cookie
        realCookie["calendar"] = json.dumps(cookie)
        realCookie["calendar"]["path"] = "/"
        #cherrypy.response.cookie["calendar"] = realCookie
        #cherrypy.response.cookie["calendar"] = json.dumps(cookie)


def decode_id_token(id_token):
    jwebtoken = jwt.decode(id_token, verify=False)
    print("jwttoken: ", jwebtoken)
    return jwebtoken

def authorize_user(useremail):
    print("authorized", useremail, config["authorization"]["user_mails"])
    return True if useremail in config["authorization"]["user_mails"] else False