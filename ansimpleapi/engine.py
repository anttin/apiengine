import cherrypy
import copy
import json
import os

from .basicauth import BasicAuth
from .defaults import DEFAULT_CONFIG

class Engine(object):

  """
    config_filename: Filename with path to the config file this engine will use

    apps:            A list of App-objects that the Engine will serve

    default_config:  A dict of default config to use for the Engine;
                     used in case config file does not already exist
  """
  def __init__(self, config_filename=None, apps=[], default_config=DEFAULT_CONFIG):
    self.apps            = apps if apps is not None else []
    self.config_filename = config_filename

    if config_filename is not None:      
      self.config = self._load_configuration(self.config_filename, default_config)
      self._save_configuration(self.config_filename, self.config)
    else:
      self.config = default_config

    # The engine_params can be used in apps to use engine provided common config sets.
    # Currently supported common config sets are:
    #   - auth: provides basic athentication based on the engine's config file's user-serction

    self.engine_params = {}

    self.auth = {}
    self.auth["basic"] = BasicAuth(self.config["users"] if "users" in self.config else {})
    self.engine_params["basicauth"] = self.auth["basic"].checkpassword 


  @classmethod
  def _recusive_join(cls, primary_dict, secondary_dict):
    for x in secondary_dict:
      if x not in primary_dict:
        primary_dict[x] = secondary_dict[x]
      elif isinstance(secondary_dict[x], dict):
        primary_dict[x] = cls._recusive_join(primary_dict[x], secondary_dict[x])
    return primary_dict


  def _load_configuration(self, filename, defaults_dict=None):
    if not os.path.isfile(filename):
      return defaults_dict if defaults_dict is not None else {} 

    data = None

    # don't care about exceptions, we're happy to fail if there is an exception
    with open(filename, encoding='utf8') as file:
      data = json.load(file)

    if defaults_dict is not None:
      d = self._recusive_join(data, defaults_dict)

    return d


  def _save_configuration(self, filename, conf_dict):
    # don't care about exceptions, the user will handle them
    with open(filename, 'w') as cfile:  
        json.dump(conf_dict, cfile, indent=4, sort_keys=True, separators=(',', ': '))
 

  def _get_app_config(self, app_name):
    app_common = copy.deepcopy(self.config["app_common"]) if "app_common" in self.config else {}
    app_specific = copy.deepcopy(self.config["app"][app_name]) if app_name in self.config["app"] else {} 
    return self._recusive_join(app_specific, app_common)


  def _mount_apps(self):
    for app in self.apps:
      self._mount(app)


  def _mount(self, app):
    app.engine_app_config = self._get_app_config(app.name)

    cherrypy.tree.mount(
      app,
      app.mountpath,
      app.get_config(self.engine_params)
    )


  def get_config(self, key):
    return self.config[key] if key in self.config else {}


  def add_app(self, app):
    self.apps.append(app)


  def run(self):
    cherrypy.config.update(self.config["server"])

    self._mount_apps()

    cherrypy.engine.start()
    cherrypy.engine.block()

