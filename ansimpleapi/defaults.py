import copy

DEFAULT_CONFIG = {
    "server": {
      "global": {
        "server.socket_host": "127.0.0.1",
        "server.socket_port": 8080,
        "server.thread_pool": 10
      }
    },
    "users": {
    },
    "app": {
    },
    "app_common": {
    }
}

DEFAULT_CONFIG_SSL = copy.deepcopy(DEFAULT_CONFIG)
DEFAULT_CONFIG_SSL["server"]["global"]["server.ssl_module"]      = '''builtin'''
DEFAULT_CONFIG_SSL["server"]["global"]["server.ssl_certificate"] = "ssl/cert.pem"
DEFAULT_CONFIG_SSL["server"]["global"]["server.ssl_private_key"] = "ssl/private_key.pem"
