
class App(object):
  def __init__(self, name, mountpath, app_config={}):
    self.name              = name
    self.mountpath         = mountpath
    self.local_app_config  = app_config

    self._engine_app_config   = None
    self._combined_app_config = app_config


  @property
  def app_config(self):
    return self._combined_app_config


  @property
  def engine_app_config(self):
    return self._engine_app_config


  @engine_app_config.setter
  def engine_app_config(self, value):
    self._engine_app_config = value
    self._combined_app_config = {
      **self._engine_app_config,
      **self.local_app_config
    }
      

  def get_config(self, engine_params={}):
    """
    Override this function to return cherrypy app config for the app.
    Use self.config_params on App-object init for config variables.
    See the Engine-class code for the available engine_params.
    """
    config = {
      '/': self.app_config
    }
    return config

