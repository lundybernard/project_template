import os
import yaml


def get_config(config_file=None):
    if config_file:
        CONF_PATH = config_file
    elif usr_conf := os.environ.get('PROJECT_CONFIG', default=None):
        CONF_PATH = usr_conf
    else:
        raise Exception(
            "Config File not specified:"
            " set environment variable PROJECT_CONFIG to config file path,"
            " or speicfy a config file."
        )

    with open(CONF_PATH) as env_file:
        CONF = yaml.load(env_file, Loader=yaml.BaseLoader)

    return CONF
