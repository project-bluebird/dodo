import os
import yaml


def find_config():
    """
    Find and parse the config.yml file.
    """
    try:
        """used for installs"""
        this_dir, this_filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(this_dir, "config.yml"), "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
    except:
        """used for development"""
        try:
            with open("../config.yml", "r") as ymlfile:
                cfg = yaml.safe_load(ymlfile)
        except:
            try:
                with open("../../config.yml", "r") as ymlfile:
                    cfg = yaml.safe_load(ymlfile)
            except:
                raise FileNotFoundError("The config file is missing.")
    return cfg


def config_param(param, config="default"):
    cfg_file = find_config()
    return cfg_file[config][param]
