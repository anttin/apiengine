
class APIApp(object):
  def __init__(self, app_config_name, mountpath, config={}, config_params={}, additional_config={}):
    self.app_config_name   = app_config_name
    self.mountpath         = mountpath
    self.config            = config
    self.config_params     = config_params
    self.additional_config = additional_config 

    self.app_config = None   


  def set_app_config(self, app_config):
    self.app_config = app_config


  def get_config(self, engine_params={}):
    """
    Override this function to return cherrypy app config for the app.
    Use self.config_params on APIApp-object init for config variables.
    Parameter engine_params has builtin configuration parameters coming from the api engine that can be used:
      - auth: builtin checkpassword function for cherrypy basic authentication
    """
    config = {
      '/': self.config
    }
    return config


####################################################################################################################


class APIAppConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)




