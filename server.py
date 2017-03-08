import os, os.path
import json
import cherrypy
from cherrypy.lib.static import serve_file
from year import cal
import authorization



class Calendar(object):
    @cherrypy.expose
    def index(self):
        print("index cookie: ", cherrypy.request.cookie, cherrypy.response.headers)
        application = cherrypy.tree.apps['/calendar']
        host = application.config['global']['index']
        print("host: ", host, application)
        return open(host)

    @cherrypy.expose
    def generate(self, **params):
        print("generate cookie: ", cherrypy.request.cookie)
        print("params", params)
        authorization.check_authorized()

        cal.set_settings(params)
        cal.generate()

        result = {"pdfUrl": "cal.pdf"}
        return json.dumps(result)


    @cherrypy.expose
    def downloadurl(self, **params):
        print("downloadurl cookie: ", cherrypy.request.cookie)
        result = {"pdfUrl": "cal.pdf"}
        return json.dumps(result)



    @cherrypy.expose
    def get_auth_request(self, provider):
        print("get_auth_request cookie: ", cherrypy.request.cookie)
        return authorization.get_authorization_url(provider)


    @cherrypy.expose
    def redirect(self, **params):
        print("redirect cookie: ", cherrypy.request.cookie)
        print("getting: ", params)
        authorization.validate_state_token(params)
        authorization.exchange_authorization_token("google", params)
        application = cherrypy.tree.apps['/calendar']
        raise cherrypy.HTTPRedirect(application.config['global']['redirectBack'])


    @cherrypy.expose
    def settings(self, **params):
        print("settings cookie: ", cherrypy.request.cookie, cherrypy.response.headers)
        print("settings headers: ", cherrypy.response.headers)
        authorization.check_authorized()
        return cal.get_settings()


if __name__ == '__main__':
    cherrypy.quickstart(root=Calendar(), script_name='/calendar', config="server.prod.config")
