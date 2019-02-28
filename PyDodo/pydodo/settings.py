"""
Settings for the Dodo app
- imported from `config.yaml` file in root directory
"""

import os
import yaml

API_VERSION = 1

this_dir, this_filename = os.path.split(os.path.abspath(__file__))
with open(os.path.join(this_dir, "config.yml"), 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

default = cfg['default']
BB_HOST = cfg['default']['host']
BB_PORT = cfg['default']['port']
