"""
Settings for the Dodo app
- imported from `config.yaml` file in root directory
"""

API_VERSION = 1

# BB_HOST = '0.0.0.0'
# BB_PORT = 5001

from os import path
import yaml

file_path = path.abspath(__file__)
root_dir = file_path.split("/PyDodo")[0]
config_file = "config.yml"

with open(root_dir+"/"+config_file, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

default = cfg['default']
BB_HOST = cfg['default']['host']
BB_PORT = cfg['default']['port']
