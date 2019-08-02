import os
import yaml


def yaml_load(ymlfile):
    """
    Load yaml file. If PyYaml version < 5, first line won't work.
    """
    try:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    except:
        cfg = yaml.load(ymlfile)
    return cfg


def find_config():
    """
    Find and parse the config.yml file.
    """
    try:
        """used for installs"""
        this_dir, this_filename = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(this_dir, "config.yml"), "r") as ymlfile:
            #cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
            cfg = yaml_load(ymlfile)
    except:
        """used for development"""
        try:
            with open("../config.yml", "r") as ymlfile:
                # cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
                cfg = yaml_load(ymlfile)
        except:
            try:
                with open("../../config.yml", "r") as ymlfile:
                    # cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
                    cfg = yaml.load(ymlfile)
            except:
                raise FileNotFoundError("The config file is missing.")
    return cfg


def config_param(param, config="default"):
    cfg_file = find_config()
    return cfg_file[config][param]
