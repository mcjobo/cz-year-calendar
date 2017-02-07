import os, os.path
import json
import cherrypy
from year import cal
import authorization



class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('static/index.html')

    @cherrypy.expose
    def generate(self, key=""):
        print(key)
        if (not authorization.authorize()):
            raise cherrypy.HTTPError(401)

        cal.generate()

        result = {"pdfUrl": "/static/cal.pdf"}
        return json.dumps(result)


    @cherrypy.expose
    def get_auth_request(self, provider):
        return authorization.get_authorization_url(provider)


    @cherrypy.expose
    def redirect(self, **params):
        print("getting: ", params)
        authorization.validate_state_token(params)
        authorization.exchange_authorization_token("google", params)
        return open('static/index.html')


if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator(), '/', "server.config")