import cherrypy
import json

from ansimpleapi.engine import Engine
from ansimpleapi.app import App

class AppBase(App):
  def __init__(self, name, mountpath, app_config):
    super().__init__(name, mountpath, app_config)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def default(self, *args, **kwargs):
    cherrypy.response.status = 404
    return {
      "status": "ERROR",
      "message": "Not Found"
    }

class AppRoot(AppBase):
  def __init__(self):
    super().__init__("root", "/", {})

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def index(self):
    cherrypy.response.status = 403
    return {
      "status": "ERROR",
      "message": "Forbidden"
    }

  @staticmethod
  def error_page_401(status, message, traceback, version):
    cherrypy.response.status = 401
    cherrypy.response.headers["Content-type"] = "text/json" 
    return json.dumps({
        "status": "ERROR",
        "message": "Unauthorized"
    })


class AppAuth(AppBase):
  def __init__(self, name, mountpath, app_config):
    super().__init__(name, mountpath, app_config)

  def get_config(self, engine_params={}):
    return {
      '/': {
        **{
          'tools.auth_basic.on': True,
          'tools.auth_basic.realm': 'localhost',
          'tools.auth_basic.checkpassword': engine_params["basicauth"]
        },
        **self.app_config
      }
    }



class Api(object):

  def __init__(self):
    self.create_apps()

  def create_apps(self):
    self.apps = [
      AppRoot(),
      AppAuth()
    ]

  def run(self):
    self.engine = Engine("config.json", self.apps)
    cherrypy.config.update({
      'error_page.401': AppRoot.error_page_401
    })
    self.engine.run()


def main(argv):
  o = Api()
  o.run()


if __name__ == "__main__":
  main(sys.argv[1:])
