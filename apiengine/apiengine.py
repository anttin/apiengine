import cherrypy
import json
import os

from apiengine.auth import Auth


class APIEngine(object):
  def __init__(self, config_filename, apps=[], default_config=None, use_defaults=False):
    self.apps            = apps if apps is not None else []
    self.config_filename = config_filename
    self.use_defaults    = use_defaults

    self.config = None
    self.default_config = {
      'server': {      
        'global': {
          'server.socket_host': '127.0.0.1', 
          'server.socket_port': 8080,
          'server.thread_pool': 10,
          'server.ssl_module'     : '''builtin''',
          'server.ssl_certificate': 'ssl/cert.pem',
          'server.ssl_private_key': 'ssl/privkey.pem'
        }
      },
      'users': {
      },
      'app': {
      },
      'global': {
      }
    } if default_config is None else default_config

    if use_defaults == True:
      self._save_configuration(self.config_filename, self.default_config)
      return  
    else:      
      self.config = self._load_configuration(self.config_filename, self.default_config)   

    self.auth = Auth(self.config['users'] if 'users' in self.config else {})

    self.engine_params = {
      'auth': self.auth.checkpassword 
    }


  def _load_configuration(self, filename, defaults_dict=None):
    if os.path.isfile(filename):
      data = None

      # don't care about exceptions, we're happy to fail if there is an exception
      with open(filename, encoding='utf8') as file:
        data = file.read()
        if data:
          d = json.loads(data)

        def recusive_defaults(conf_dict, def_dict):
          for x in def_dict:
            if x not in conf_dict:
              conf_dict[x] = def_dict[x]
            elif isinstance(def_dict[x], dict):
              conf_dict[x] = recusive_defaults(conf_dict[x], def_dict[x])
          return conf_dict

        if defaults_dict is not None:
          d = recusive_defaults(d, defaults_dict)

        return d

    return defaults_dict if defaults_dict is not None else {} 


  def _save_configuration(self, filename, conf_dict):
    # don't care about exceptions, the user will handle them
    with open(filename, 'w') as cfile:  
        json.dump(conf_dict, cfile, indent=4, sort_keys=True, separators=(',', ': '))
 

  def _get_app_config(self, app_name, default_value={}):
    global_cfg = self.config['global'] if 'global' in self.config else {}
    app_cfg    = self.config['app'][app_name] if app_name in self.config['app'] else default_value
    return { **global_cfg, **app_cfg } 


  def _mount_apps(self):
    for app in self.apps:
      self._mount(app)


  def _mount(self, apiapp_obj):
    apiapp_obj.set_app_config({ **self._get_app_config(apiapp_obj.app_config_name), **apiapp_obj.additional_config })
    cherrypy.tree.mount(apiapp_obj, apiapp_obj.mountpath, apiapp_obj.get_config(self.engine_params))


  def get_config(self, key):
    return self.config[key] if key in self.config else {}


  def add_apps(self, apps):
    for app in apps:
      self.apps.append(app)


  def run(self):
    cherrypy.config.update(self.config['server'])

    self._mount_apps()

    cherrypy.engine.start()
    cherrypy.engine.block()

