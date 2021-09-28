import cherrypy

from apiengine.apiapp import APIApp

class APIRoot(APIApp):
  def __init__(self, app_config_name='root', mountpath='/', config={}, config_params={}, additional_config={}):
    super().__init__(app_config_name, mountpath, config, config_params, additional_config)

  @cherrypy.expose
  def index(self):
    raise cherrypy.HTTPError(status=403)


