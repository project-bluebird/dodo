"""
Settings for the Dodo app
- imported from `config.yaml` file in root directory
"""

import os
import yaml

API_VERSION = 1

this_dir, this_filename = os.path.split(os.path.abspath(__file__))
try:
    """used for installs"""
    with open(os.path.join(this_dir, "config.yml"), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
except:
    """used for development"""
    try:
        with open("../config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except:
        try:
            with open("../../config.yml", 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
        except:
            raise FileNotFoundError("The config file is missing.")

default = cfg['default']
BB_HOST = cfg['default']['host']
BB_PORT = cfg['default']['port']
