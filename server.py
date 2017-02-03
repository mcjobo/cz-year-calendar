import os, os.path
import json
import cherrypy
from year import cal

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('static/index.html')

    @cherrypy.expose
    def generate(self, key=""):
        print(key)

        #cal.generate()

        result = {"pdfUrl": "/static/cal.pdf"}
        return json.dumps(result)




if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }
    cherrypy.quickstart(StringGenerator(), '/', conf)