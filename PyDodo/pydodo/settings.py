"""
Settings for the Dodo app
- imported from `config.yaml` file in root directory
"""

import os
import yaml

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
HOST = cfg['default']['host']
PORT = cfg['default']['port']
API_VERSION = cfg['default']['api_version']
API_PATH = cfg['default']['api_path']
SIMULATOR = cfg['default']['simulator']
