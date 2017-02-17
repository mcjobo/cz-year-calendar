import os, os.path
import json
import cherrypy
from year import cal
import authorization



class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('static/index2.html')

    @cherrypy.expose
    def generate(self, **params):
        print("params", params)
        authorization.check_authorized()

        cal.set_settings(params)
        cal.generate()

        result = {"pdfUrl": "/static/cal.pdf"}
        return json.dumps(result)


    @cherrypy.expose
    def downloadurl(self, **params):
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
        return open('static/index2.html')


    @cherrypy.expose
    def settings(self, **params):
        authorization.check_authorized()
        return cal.get_settings()


if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator(), '/', "server.config")